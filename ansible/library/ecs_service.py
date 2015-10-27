#!/usr/bin/python

import boto3, datetime

def create_service(module):
    region          = module.params.get('region')
    cluster         = module.params.get('cluster')
    name            = module.params.get('name')
    definition      = module.params.get('definition')
    load_balancers  = module.params.get('load_balancers')
    desired_count   = module.params.get('desired_count')
    role            = module.params.get('role')
    token           = module.params.get('token')
    ecs             = boto3.client('ecs', region_name=region)

    services = ecs.describe_services(cluster=cluster, services=[name])
    kwargs = dict(
        cluster        = cluster,
        service        = name,
        taskDefinition = definition,
        desiredCount   = desired_count
    )

    if len(services['services']):
        return ecs.update_service(**kwargs)

    else:
        del kwargs['service']
        kwargs.update(serviceName=name)

        if len(load_balancers):
            kwargs.update(loadBalancers=load_balancers, role=role)

        if token:
            kwargs.update(clientToken=token)

        return ecs.create_service(**kwargs)

def main():
    module = AnsibleModule(
        argument_spec = dict(
            region          = dict(required=True),
            cluster         = dict(required=True),
            name            = dict(required=True),
            definition      = dict(required=True),
            load_balancers  = dict(default=[]),
            desired_count   = dict(default=1, type='int'),
            role            = dict(required=True),
            token           = dict()
        )
    )

    try:
        response = create_service(module)
        module.exit_json(service_arn=response['service']['serviceArn'])

    except Exception as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
