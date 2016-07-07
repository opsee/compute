#!/usr/bin/env python

from os import path
import json
import boto3
import botocore
import click

def build_config(region, environment, stack_name):
    config = {'environment': environment, 'region': region}
    global_cf_path = path.join('config', 'global.json')
    if path.isfile(global_cf_path):
        with open(global_cf_path) as f:
            config.update(json.load(f))

    region_cf_path = path.join('config', 'region', '%s.json' % region)
    if path.isfile(region_cf_path):
        with open(region_cf_path) as f:
            config.update(json.load(f))

    env_cf_path = path.join('config', 'environment', '%s.json' % environment)
    if path.isfile(env_cf_path):
        with open(env_cf_path) as f:
            config.update(json.load(f))

    service_cf_path = path.join('config', 'service', '%s.json' % stack_name)
    if path.isfile(service_cf_path):
        with open(service_cf_path) as f:
            config.update(json.load(f))

    return config

@click.command()
@click.argument('stack_name')
@click.option('--environment', default='production', help='Opsee environment')
@click.option('--region', default='us-west-2', help='AWS Region')
def deploy(stack_name, environment, region):
    stack_module = __import__(stack_name)

    cfn_stack_name = '%s-%s' % (stack_name, environment)
    config = build_config(region, environment, stack_name)

    cfn = boto3.client('cloudformation', region_name=region)

    template_json = stack_module.Stack(config).to_json()
    print template_json

    create_or_update_args = {'StackName': cfn_stack_name, 'TemplateBody': template_json, 'Tags': [{'Key': 'Environment', 'Value': environment}]}
    wait_state = ''

    stack_exists = True
    try:
        cfn.describe_stacks(StackName=cfn_stack_name)
    except botocore.exceptions.ClientError:
        stack_exists = False

    if not stack_exists:
        cfn.create_stack(**create_or_update_args)
        wait_state = 'stack_create_complete'
    else:
        cfn.update_stack(**create_or_update_args)
        wait_state = 'stack_update_complete'

    waiter = cfn.get_waiter(wait_state)
    waiter.wait(StackName=cfn_stack_name)

    print 'Stack update complete.'


if __name__ == '__main__':
    deploy(auto_envvar_prefix='DEPLOY')