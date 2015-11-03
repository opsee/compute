Ansible
=======

Prerequisites
-------------

Exported AWS environment vars:
```
AWS_DEFAULT_REGION
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

Running playbooks
-----------------

To run playbooks, first build the docker image with `make build` and run the playbook with `./run [playbook] [optional args]`. e.g.

```
# this runs the tasks tagged with strongswan in the coreos-production playbook
make build && ./run coreos-production -t strongswan

# this runs the tasks tagged with coreos-cluster with more verbosity in the coreos-production playbook
make build && ./run coreos-production -t coreos-cluster -vvv
```

Unfortunately, for now we have to build the docker container every time since mounting volumes is unreliable with docker-machine.

Playbook: coreos-production
---------------------------

This configures a 3-node etcd quorum, 2 ecs worker nodes, and a strongswan vpn instance into us-west-2.