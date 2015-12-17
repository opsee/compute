from troposphere import Template, Ref, Parameter, GetAtt
import troposphere.ecs as ecs
import troposphere.ec2 as ec2

import boto3
#import opsee.helpers as helpers

ecs_linux_ami_map = {
  'us-west-2': 'ami-52180c33',
  'us-east-1': 'ami-5449393e'
}

subnet_map = {
  'us-west-2': {
    'us-west-2a': '172.30.0.0/20',
    'us-west-2b': '172.30.16.0/20',
    'us-west-2c': '172.30.32.0/20'
  }
}

config = {
  'region': 'us-west-2',
  'environment': 'staging',
}

region = config['region']
environment = config['environment']

# VPC, Subnets, IGW, Routes, 
t = Template()

environment_param = t.add_parameter(Parameter(
  'Environment',
  Description='Name of the environment (e.g. staging, production)',
  Type='String',
))

vpc = t.add_resource(ec2.VPC(
  'OpseeVPC', 
  CidrBlock='172.30.0.0/16',
  Tags=[
    {
      'Key': 'Environment', 
      'Value': Ref(environment_param),
    },
  ],
))

igw = t.add_resource(ec2.InternetGateway(
  'IGW',
  Tags=[
    {
      'Key': 'VPC',
      'Value': Ref(vpc),
    },
    {
      'Key': 'Environment', 
      'Value': Ref(environment_param),
    },
  ],
))

t.add_resource(ec2.VPCGatewayAttachment(
  'IGWAttachment',
  VpcId=Ref(vpc),
  InternetGatewayId=Ref(igw),
))

route_table = t.add_resource(ec2.RouteTable(
  'RouteTable',
  VpcId=Ref(vpc),
  Tags=[
    {
      'Key': 'VPC',
      'Value': Ref(vpc),
    },
    {
      'Key': 'Environment', 
      'Value': Ref(environment_param),
    },
  ],
))

t.add_resource(ec2.Route(
  'InternetRoute',
  DestinationCidrBlock='0.0.0.0/0',
  GatewayId=Ref(igw),
  RouteTableId=Ref(route_table),
))

for az in subnet_map[region]:
  subnet_name = 'Subnet%s' % az.split('-')[-1]

  r = subnet_map[region]
  subnet = t.add_resource(ec2.Subnet(
    subnet_name,
    AvailabilityZone=az, 
    CidrBlock=r[az], 
    MapPublicIpOnLaunch=False, 
    Tags=[
      {
        'Key': 'Environment',
        'Value': Ref(environment_param),
      },
    ],
    VpcId=Ref(vpc),
  ))

  t.add_resource(ec2.SubnetRouteTableAssociation(
    '%sRTAssociation' % subnet_name,
    RouteTableId=Ref(route_table),
    SubnetId=Ref(subnet),
  ))

# SG for cluster

# internal vpn security group

# bastion vpn security group

# SG for internal LBs 

sg = t.add_resource(ec2.SecurityGroup(
  'InternalELBSecurityGroup',
  GroupDescription='%s - %s - Internal ELB Security Group' % (region, environment),
  SecurityGroupEgress=[
    {
      CidrIp: '0.0.0.0/0',
      IpProtocol='-1',
    },
  ],
  SecurityGroupIngress=[
    # cluster security group
    # internal vpn security group
    # bastion vpn security group
  ],
  Tags=[
    {
      'Key': 'Environment',
      'Value': Ref(environment_param),
    },
  ],
  VpcId=Ref(vpc),
))

# SG for external LBs 


# Keypair

# IAM Roles

# ECS Linux instances


client = boto3.client('cloudformation')
response = client.create_stack(
  StackName=environment,
  TemplateBody=t.to_json(),
  
  Parameters=[
    {
      'ParameterKey': 'Environment',
      'ParameterValue': environment,
      'UsePreviousValue': True,
    },
  ],
  Capabilities=[
    'CAPABILITY_IAM',
  ],
  OnFailure='ROLLBACK',
  Tags=[
    {
      'Key': 'Environment',
      'Value': environment,
    },
  ]
)
