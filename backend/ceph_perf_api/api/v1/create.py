# -*- coding: UTF-8 -*-
import time
import re
import json
import os
import sys

import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models as fiomodels
from ITuning_ceph_deploy import models as deploymodels
from job_conductor import api as job_api
from fiotest.fio_test import build_suite
from fiotest.fio_test import run_suite

@urls.register
class CreateFioJob(generic.View):
    url_regex = r'^create$'


    def __init__(self):
        self.job_conductor = job_api.API()

    def create_suite(self, body):
        if body['fiopara']:
            other_fio_config = body['fiopara'].split('\n')
        else:
             other_fio_config = []

        fiotest = build_suite.FIOTest()

        dir_path, create_time = fiotest.create_suite_dir(body['jobname'])

        with open('{}/fioserver_list.conf'.format(dir_path), 'w') as f:
            for client in body['client']:
                f.write(client)
                f.write('\n')

        if body['cephconfig'] == 'default':
            cephconfig = ['default']
        else:
            config = re.sub('\n', ';', body['cephconfig'])
            cephconfig = [config]
        fiotest.gen_setup_ceph_config(dir_path, cephconfig)

        casenum = 1
        for rw in body['fiotype']:
            for bs in body['bs']:
                for iodepth in body['iodepth']:
                    for numjob in body['numjob']:
                        for rwmixread in body['rwmixread']:
                            fiotest.case(
                                dir_path,
                                casenum,
                                body['poolname'],
                                rw,
                                bs,
                                body['runtime'],
                                str(iodepth),
                                str(numjob),
                                body['imagecount'],
                                body['jobname'],
                                rwmixread,
                                body['imagename'],
                                body['client'],
                                other_fio_config,
                            )
                            casenum = casenum + 1
        return dir_path, create_time


    @utils.json_response
    def post(self, request):
        body = request.DATA
        print body

        if not body.has_key('cephconfig') or body['cephconfig'] == '':
            body['cephconfig'] = 'default'
        if not body.has_key('fiopara') or body['fiopara'] == '':
            body['fiopara'] = None
        if not body.has_key('sysdata') or body['sysdata'] == '':
            body['sysdata'] = []
        suite_dir, create_time = self.create_suite(body)
        
        result = deploymodels.Cluster.objects.filter(clustername=body['cluster']).all()[0]
        body['cluster'] = result.id
        runfio = run_suite.RunFIO(suite_dir, result.id)
        runfio.checkandstart_fioser_allclient()

        body['suite_dir'] = suite_dir

        ceph_config_file = '{}/setup_ceph_config.json'.format(suite_dir)
        jobinfo = {
            'name': body['jobname'],
            'status': "New",
            'createtime': create_time,
            'testdir': suite_dir,
            'jobdir': suite_dir.split('/')[-1],
            'cluster': result.clustername,
            'ceph_config': body['cephconfig'],
            'fiopara': body['fiopara'],
            'sysdata': str(body['sysdata'])
        }
        if os.path.exists(ceph_config_file):
            ceph_configs = json.load(open(ceph_config_file))
            for ceph_config in ceph_configs:
                body['ceph_config'] = ceph_config
                result = fiomodels.Jobs.objects.create(**jobinfo)
                body['jobid'] = result.id
                self.job_conductor.run_fio(body)
        else:
            result = fiomodels.Jobs.objects.create(**jobinfo)
            body['jobid'] = result.id
            self.job_conductor.run_fio(body)

        return "pass"

    @utils.json_response
    def options(self, request):
        return "option"

