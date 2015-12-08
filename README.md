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

To run playbooks, first make sure your ansible environment is setup by running `make`.

This will prompt you for a PGP passphrase to decrypt the Ansible Vault password. This is either a passphrase you set yourself or your Keybase passphrase.

You should see output that looks something like:
```
λ make
New python executable in .env/bin/python
Installing setuptools, pip, wheel...done.
Obtaining Ansible from git+https://github.com/ansible/ansible.git@stable-2.0#egg=Ansible (from -r requirements.txt (line 1))
  Cloning https://github.com/ansible/ansible.git (to stable-2.0) to ./.env/src/ansible

... Whole bunch of deps get ...

Installing collected packages: ecdsa, pycrypto, paramiko, MarkupSafe, Jinja2, PyYAML, setuptools, Ansible, boto, jmespath, futures, six, python-dateutil, docutils, botocore, boto3, httplib2, netaddr
  Found existing installation: setuptools 18.2
    Uninstalling setuptools-18.2:
      Successfully uninstalled setuptools-18.2
  Running setup.py develop for Ansible
Successfully installed Ansible Jinja2-2.8 MarkupSafe-0.23 PyYAML-3.11 boto-2.38.0 boto3-1.2.2 botocore-1.3.11 docutils-0.12 ecdsa-0.13 futures-2.2.0 httplib2-0.9.2 jmespath-0.9.0 netaddr-0.7.18 paramiko-1.16.0 pycrypto-2.6.1 python-dateutil-2.4.2 setuptools-18.7.1 six-1.10.0

Execute: source .env/bin/activate
```

After running `source .env/bin/activate`, you can then run playbooks.

Run the playbook with `./run [playbook] [optional args]`. e.g.

```
# this runs the tasks tagged with strongswan in the coreos-production playbook
make build && ./run coreos-production -t strongswan

# this runs the tasks tagged with coreos-cluster with more verbosity in the coreos-production playbook
make build && ./run coreos-production -t coreos-cluster -vvv
```

Playbook: coreos-production
---------------------------

This configures a 3-node etcd quorum, 2 ecs worker nodes, and a strongswan vpn instance into us-west-2.

Vault
-----

The default `make` target should decrypt your Vault password for you, but here are instructions for manually working with passphrases.

The vault passphrase can be encrypted/decrypted using keybase.

```
λ brew install keybase

...

λ keybase login

λ keybase pgp decrypt -i vault_password/$(whoami).gpg > .vault_password

You need a passphrase to unlock the secret key for
user: "keybase.io/keybase_username <keybase_username@keybase.io>"
4096-bit RSA key, ID 5C6CDEF4362A772F, created 2015-11-03
         (subkey on main key ID D25BB76C14050BD0)

Enter passphrase: <enter passphrase, hit enter>

λ ansible-vault edit secrets/app-env.yml

```

If you need to onboard a new person to the Ansible vault, do this:

```
keybase pgp encrypt -i .vault_password "their keybase username" > vault_password/their_computer_username.gpg
```
