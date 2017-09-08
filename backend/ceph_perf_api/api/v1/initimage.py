# -*- coding: UTF-8 -*-
import os
import sys
import yaml
import subprocess

import urls
from django.views import generic
from ceph_perf_api import utils
from job_conductor import api as job_api

@urls.register
class InitImage(generic.View):
    url_regex = r'^initimage/(?P<id>\d+)/$'

    def __init__(self):
        self.job_conductor = job_api.API()

    @utils.json_response
    def get(self, request, id):
        hwinfo_file = '{}/../../{}_ceph_hw_info.yml'.format(
            os.path.dirname(os.path.realpath(__file__)),
            id)
        with open(hwinfo_file, 'r') as f:
            ceph_info = yaml.load(f)
        client = ceph_info['ceph-client'].popitem()
        client_ip = client[1]['ip']
        client_password = client[1]['password']

        cmd = "ssh {} 'rbd du'".format(client_ip)
        output = subprocess.check_output(cmd, shell=True)

        return {"total": len(d), "data": output}


    @utils.json_response
    def post(self, request, id):
        body = dict(request.DATA)
        print body
        body['clusterid'] = id
        self.job_conductor.initimage(body)
        return "pass"

    @utils.json_response
    def options(self, request, id):
        return "option"
