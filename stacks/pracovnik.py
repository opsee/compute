#!/usr/bin/env python

import json
import os
from os import path

import troposphere
import troposphere.ecs as ecs

class Stack(object):
    ServiceName = 'pracovnik'

    def __init__(self, config):
        self.t = troposphere.Template()
        self.config = config
        self.env = config['environment']
        self.region = config['region']
        self._template()

    def _template(self):
        task = ecs.TaskDefinition('%s%sTask' % (self.ServiceName.title(), self.env.title()))
        container = ecs.ContainerDefinition()
        container.Name = self.ServiceName
        container.Image = self.config['image']
        container.Memory = self.config['memory']
        if self.config.get('cpu', '') != '':
            container.Cpu = self.config['cpu']
        container.LogConfiguration = ecs.LogConfiguration(
            LogDriver='syslog',
            Options={
                "syslog-address": self.config['syslog-address'],
                "tag": self.ServiceName,
                "syslog-tls-skip-verify": "true",
            }
        )
        container.Command = self.config['command']
        container.Environment = [ecs.Environment(Name='APPENV', Value='%senv-%s-%s' % (self.ServiceName, self.env, self.region))]

        task.ContainerDefinitions = [container]
        self.t.add_resource(task)

        service = ecs.Service('%s%sService' % (self.ServiceName.title(), self.env.title()))
        service.Cluster = '%s-%s' % (self.env, self.region)
        service.DeploymentConfiguration = ecs.DeploymentConfiguration(MaximumPercent=200, MinimumHealthyPercent=100)
        service.DesiredCount = 2
        service.TaskDefinition = troposphere.Ref(task)
        self.t.add_resource(service)

    def to_json(self):
        return self.t.to_json()
