#!/usr/bin/python

import boto3

def fetch_facts(module):
    region            = module.params.get('region')
    elb               = boto3.client('elb', region_name=region)

    elbs = elb.describe_load_balancers()['LoadBalancerDescriptions']
    for e in elbs:
        del e['CreatedTime']

    return elbs

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name              = dict(),
            id                = dict(),
            region            = dict(required=True)
        )
    )

    try:
        facts = fetch_facts(module)
        module.exit_json(elbs=facts)

    except Exception as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
