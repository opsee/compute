#!/usr/bin/python

import boto3

def fetch_facts(module):
    vpc_id            = module.params.get('vpc_id')
    region            = module.params.get('region')
    name              = module.params.get('name')
    rds               = boto3.client('rds', region_name=region)

    groups = [group for group in rds.describe_db_subnet_groups()['DBSubnetGroups'] if group['VpcId'] == vpc_id]
    if name:
        groups = [group for group in groups if group['DBSubnetGroupName'] == name][0]

    return groups

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name              = dict(),
            vpc_id            = dict(required=True),
            region            = dict(required=True)
        )
    )

    try:
        facts = fetch_facts(module)
        module.exit_json(facts=facts)

    except Exception as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
