# -*- coding: UTF-8 -*-
import time
import re
import json
import os
import sys

import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models
from job_conductor import api as job_api
from fiotest.fio_test import build_suite
from fiotest.fio_test import run_suite

@urls.register
class CreateFioJob(generic.View):
    url_regex = r'^create$'


    def __init__(self):
        self.job_conductor = job_api.API()

    def create_suite(self, body):
        body['clientkeys'].append(1)
        clientslist = []
        for clientkey in body['clientkeys']:
            clientslist.append(body['client-{}'.format(clientkey)])

        other_fio_config = []
        for fiokey in body['fioparakeys']:
            other_fio_config.append(body['fiopara-{}'.format(fiokey)])

        fiotest = build_suite.FIOTest()

        dir_path = fiotest.create_suite_dir(body['jobname'])

        with open('{}/fioserver_list.conf'.format(dir_path), 'w') as f:
            for client in clientslist:
                f.write(client)
                f.write('\n')

        cephconfig = []
        if len(body['cephconfigkeys']) == 0:
            cephconfig.append('default')
        for key in body['cephconfigkeys']:
            config = re.sub('\n', ';', body['cephconfig-{}'.format(key)])
            cephconfig.append(config)

        fiotest.gen_setup_ceph_config(dir_path, cephconfig)


        body['rwmixreadkeys'].append(1)

        casenum = 1
        for rw in body['fiotype']:
            for bs in body['bs']:
                for iodepth in body['iodepth']:
                    for numjob in body['numjob']:
                        for rwmixreadkey in body['rwmixreadkeys']:
                            fiotest.case(
                                dir_path,
                                casenum,
                                body['PoolName'],
                                rw,
                                bs,
                                body['Runtime'],
                                str(iodepth),
                                str(numjob),
                                body['Image Count'],
                                body['jobname'],
                                body['rwmixread-{}'.format(rwmixreadkey)],
                                body['Image Name'],
                                clientslist,
                                other_fio_config,
                            )
                            casenum = casenum + 1
        return dir_path


    @utils.json_response
    def post(self, request):
        body = request.DATA
        print body

        suite_dir = self.create_suite(body)
        runfio = run_suite.RunFIO(suite_dir, todb=True)
        runfio.checkandstart_fioser(suite_dir, body['jobname'])

        body['suite_dir'] = suite_dir

        ceph_config_file = '{}/setup_ceph_config.json'.format(suite_dir)
        if os.path.exists(ceph_config_file):
            ceph_configs = json.load(open(ceph_config_file))
            for ceph_config in ceph_configs:
                body['ceph_config'] = ceph_config
                jobinfo = {'name': body['jobname'], 'status': "New", 'createtime': suite_dir.split('_')[1]}
                result = models.Jobs.objects.create(**jobinfo)
                body['jobid'] = result.id
                self.job_conductor.run_fio(body)
        else:
            jobinfo = {'name': body['jobname'], 'status': "New"}
            result = models.Jobs.objects.create(**jobinfo)
            body['jobid'] = result.id
            self.job_conductor.run_fio(body)

        return "pass"

    @utils.json_response
    def options(self, request):
        return "option"

