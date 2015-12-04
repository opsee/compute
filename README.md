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

Vault
-----

The vault passphrase can be decrypted using keybase.

```
λ brew install keybase

...

λ keybase login

λ keybase decrypt vault_passphrase/<username>.gpg > .vault_password

You need a passphrase to unlock the secret key for
user: "keybase.io/keybase_username <keybase_username@keybase.io>"
4096-bit RSA key, ID 5C6CDEF4362A772F, created 2015-11-03
         (subkey on main key ID D25BB76C14050BD0)

Enter passphrase: <enter passphrase, hit enter>

λ ansible-vault edit secrets/app-env.yml

```

This will bring up $EDITOR and allow you to make changes to the vault.
