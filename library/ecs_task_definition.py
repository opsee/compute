#!/usr/bin/python

import boto3

def register_task(module):
    region            = module.params.get('region')
    family            = module.params.get('family')
    definitions       = module.params.get('definitions')
    volumes           = module.params.get('volumes')
    ecs               = boto3.client('ecs', region_name=region)

    return ecs.register_task_definition(family=family, containerDefinitions=definitions, volumes=volumes)

def main():
    module = AnsibleModule(
        argument_spec = dict(
            region            = dict(required=True),
            family            = dict(required=True),
            definitions       = dict(required=True),
            volumes           = dict(default=[])
        )
    )

    try:
        response = register_task(module)
        module.exit_json(response=response)

    except Exception as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
