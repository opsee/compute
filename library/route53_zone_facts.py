#!/usr/bin/python

import boto3

def fetch_facts(module):
    region            = module.params.get('region')
    name              = module.params.get('name')
    route53           = boto3.client('route53', region_name=region)

    zones = route53.list_hosted_zones_by_name(DNSName=name)
    return zones['HostedZones']

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
        module.exit_json(zones=facts)

    except Exception as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
