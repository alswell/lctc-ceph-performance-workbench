# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Cluster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(null=True)
    public_network = models.CharField(max_length=100, null=True)
    cluster_network = models.CharField(max_length=100, null=True)
    objectstore = models.CharField(max_length=20, null=True)
    journal_size = models.IntegerField(null=True)
    osdhosts = models.CharField(max_length=100, null=True)
    clients = models.CharField(max_length=100, null=True)
    mons = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=200, null=True)
    health = models.CharField(max_length=200, null=True)

class diskInfo(models.Model):
    id = models.AutoField(primary_key=True)
    clusterid = models.ForeignKey("Cluster",to_field='id', null=True)
    osdhost = models.CharField(max_length=100, null=True)
    osddisk = models.CharField(max_length=100, null=True)
    journaldisk = models.CharField(max_length=100, null=True)
