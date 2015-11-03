#!/usr/bin/python

import boto3, time

def update_instance(module):
    vpc_id            = module.params.get('vpc_id')
    private_ip        = module.params.get('private_ip')
    tags              = module.params.get('tags')
    user_data         = module.params.get('user_data')
    wait_extra        = module.params.get('wait')
    region            = module.params.get('region')
    ec2               = boto3.resource('ec2', region_name=region)

    if private_ip:
        filters = [
            {'Name': 'private-ip-address', 'Values': [private_ip]},
            {'Name': 'vpc-id', 'Values': [vpc_id]}
        ]
    elif tags:
        filters = []
        for k, v in tags.items():
            filters.append({'Name': 'tag:'+k, 'Values': [v]})

        filters.append({'Name': 'vpc-id', 'Values': [vpc_id]})

    for instance in ec2.instances.filter(Filters=filters):
        current_user_data = instance.describe_attribute(Attribute='userData')['UserData']
        if user_data == current_user_data:
            return False, instance

        instance.stop()
        instance.wait_until_stopped()
        instance.modify_attribute(UserData={'Value':user_data})
        instance.start()
        instance.wait_until_running()

        if wait_extra:
            time.sleep(wait_extra)

        return True, instance

    module.fail_json(msg='No instances found.')

def main():
    module = AnsibleModule(
        argument_spec = dict(
            user_data         = dict(required=True),
            private_ip        = dict(),
            tags              = dict(),
            wait              = dict(type='int'),
            vpc_id            = dict(required=True),
            region            = dict(required=True)
        )
    )

    try:
        (changed, instance) = update_instance(module)
        module.exit_json(changed=changed,instance_id=instance.id)

    except Exception as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
