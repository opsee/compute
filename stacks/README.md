# Stacks

Manage CloudFormation stacks

## Configuration

Configuration hashes are store as JSON files in the `config` directory. There
is, of course, a precedence to the building of the final configuration dictionary.

- global
- region
- environment
- service

The configuration hash is built in that order, so service JSON files get the last
word in how services are configured. There are two special variables that get put
into the configuration dictionary:

- `config['environment']`
- `config['region']`

Those can be used in service template creation.

## deploy.rb

The deploy script is used for managing CloudFormation stacks of all kinds. Each stack
corresponds to a Python file in the stacks directory. For example, to deploy the
pracovnik service you would run:

`./deploy.py --region <region> --environment <environment> pracovnik`

The default region is `us-west-2`.

The default environment is `production`.

See `./deploy.py --help` for more information.