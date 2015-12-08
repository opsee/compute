#!/usr/bin/env bash

# Make a best guess if we need to sudo or not
sudo=""
if [ $(which python) == "/usr/bin/python" ] && [ $(uname -s) == "Darwin" ] ; then
  sudo="sudo"
fi

# Force people to keep awscli and virtualenv up to date.
if [ ! -x $(which virtualenv) ]; then
  $sudo pip install -U virtualenv
fi

if [ ! -x $(which aws) ]; then
  $sudo pip install -U awscli
fi

if [ ! -x $(which s3kms) ]; then
  curl -Lo /opt/bin/s3kms https://s3-us-west-2.amazonaws.com/opsee-releases/go/vinz-clortho/s3kms-linux-amd64
  curl -Lo chmod +x /opt/bin/s3kms
fi

# Setup a clean virtualenv if they need it.
if [ ! -d .env ]; then
  virtualenv --no-site-packages --distribute .env
fi

source .env/bin/activate

if [ -f requirements.txt ]; then
  pip install -U -r requirements.txt
fi
