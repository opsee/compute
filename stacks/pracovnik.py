#!/usr/bin/env python

import json
import os
from os import path

import troposphere
import troposphere.ecs as ecs
import troposphere.s3 as s3

class Stack(object):
    ServiceName = 'pracovnik'

    def __init__(self, config):
        self.t = troposphere.Template()
        self.config = config
        self.env = config['environment']
        self.region = config['region']
        self._template()

    def _template(self):
        latest_results_bucket_name = '%s-%s' % (self.config['results-s3-bucket-latest'], self.env)
        latest_bucket = s3.Bucket('LatestResultsBucket%s' % self.env.title())
        latest_bucket.AccessControl = 'Private'
        latest_bucket.BucketName = latest_results_bucket_name
        latest_bucket.Tags = s3.Tags(environment=self.env)
        self.t.add_resource(latest_bucket)

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
        container.Environment = [
            # TODO(greg): could probably clean this up in cats by making the postgres conn thing better idk.
            ecs.Environment(Name='APPENV', Value='catsenv-%s-%s' % (self.env, self.region)),
            ecs.Environment(Name='CATS_RESULTS_S3_BUCKET', Value=latest_results_bucket_name)
        ]

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
