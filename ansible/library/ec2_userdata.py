#!/usr/bin/python

import boto3, time

def update_instance(module):
    vpc_id            = module.params.get('vpc_id')
    private_ip        = module.params.get('private_ip')
    availability_zone = module.params.get('availability_zone')
    user_data         = module.params.get('user_data')
    region            = module.params.get('region')
    ec2               = boto3.resource('ec2', region_name=region)

    if private_ip:
        filters = [
            {'Name': 'private-ip-address', 'Values': [private_ip]},
            {'Name': 'vpc-id', 'Values': [vpc_id]}
        ]
    elif availability_zone:
        filters = [
            {'Name': 'availability-zone', 'Values': [availability_zone]},
            {'Name': 'vpc-id', 'Values': [vpc_id]}
        ]

    for instance in ec2.instances.filter(Filters=filters, MaxResults=6):
        current_user_data = instance.describe_attribute(Attribute='userData')['UserData']
        if user_data == current_user_data:
            return False, instance

        instance.stop()
        instance.wait_until_stopped()
        instance.modify_attribute(UserData={'Value':user_data})
        instance.start()
        instance.wait_until_running()

        return True, instance

    module.fail_json(msg='No instances found.')

def main():
    module = AnsibleModule(
        argument_spec = dict(
            user_data         = dict(required=True),
            private_ip        = dict(),
            availability_zone = dict(),
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
