# -*- coding: UTF-8 -*-
import os
import re
import time
import json

import urls
from django.views import generic
from ceph_perf_api import utils
from mysql import models
from fiotest.fio_test import build_suite
from fiotest.fio_test import run_suite

@urls.register
class UserInfos(generic.View):
    url_regex = r'^create$'

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


        body['fiotypekeys'].append(1)
        body['bskeys'].append(1)
        body['iodepthkeys'].append(1)
        body['numjobkeys'].append(1)
        body['rwmixreadkeys'].append(1)

        casenum = 1
        for rwkey in body['fiotypekeys']:
            for bskey in body['bskeys']:
                for iodepthkey in body['iodepthkeys']:
                    for numjobkey in body['numjobkeys']:
                        for rwmixreadkey in body['rwmixreadkeys']:
                            fiotest.case(
                                dir_path,
                                casenum,
                                body['PoolName'],
                                body['fiotype-{}'.format(rwkey)],
                                body['bs-{}'.format(bskey)],
                                body['Runtime'],
                                str(body['iodepth-{}'.format(iodepthkey)]),
                                str(body['numjob-{}'.format(numjobkey)]),
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
        print time.localtime(time.time())

        suite_dir = self.create_suite(body)

        runfio = run_suite.RunFIO(suite_dir, todb=True)
        runfio.checkandstart_fioser(suite_dir, body['jobname'])

        ceph_config_file = '{}/setup_ceph_config.json'.format(suite_dir)
        if os.path.exists(ceph_config_file):
            ceph_configs = json.load(open(ceph_config_file))
            for ceph_config in ceph_configs:
                log_dir  = runfio.run(suite_dir, body['jobname'], ceph_config=ceph_config)
                time.sleep(2)
                runfio.gen_result(log_dir)
                runfio.store_logfile_FS(log_dir)
        else:
            log_dir = runfio.run(suite_dir, body['jobname'])
            time.sleep(2)
            runfio.gen_result(log_dir)
            runfio.store_logfile_FS(log_dir)
        print "finish"

        return "pass"

    @utils.json_response
    def options(self, request):
        return "option"

