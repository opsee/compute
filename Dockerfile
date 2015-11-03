FROM gliderlabs/alpine:3.2

RUN apk update && apk add git bash python python-dev py-pip build-base perl sudo curl \
        && rm -rf /var/cache/apk/*
RUN sudo pip install --upgrade pip \
        && sudo pip install paramiko PyYAML Jinja2 httplib2 six boto boto3 netaddr
RUN mkdir -p /opt && git clone git://github.com/ansible/ansible.git /opt/ansible --recursive
RUN mkdir -p /opt/bin && \
        curl -Lo /opt/bin/ec2-env https://s3-us-west-2.amazonaws.com/opsee-releases/go/ec2-env/ec2-env && \
        curl -Lo /opt/bin/s3kms https://s3-us-west-2.amazonaws.com/opsee-releases/go/vinz-clortho/s3kms-linux-amd64 && \
        chmod +x /opt/bin/ec2-env && \
        chmod +x /opt/bin/s3kms

ENV ANSIBLE_HOME /opt/ansible
ENV PYTHONPATH "/usr/lib/python2.7/site-packages:$ANSIBLE_HOME/lib"
ENV PATH "$ANSIBLE_HOME/bin:$PATH"
ENV MANPATH "$ANSIBLE_HOME/docs/man:$MANPATH"

ADD . /ansible
WORKDIR /ansible
ENTRYPOINT ["ansible-playbook"]
