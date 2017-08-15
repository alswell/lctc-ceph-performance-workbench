# -*- coding: UTF-8 -*-
import re
import urls
from django.views import generic
from ceph_perf_api import utils
from mysql import models
from fiotest.fio_test import build_suite

@urls.register
class UserInfos(generic.View):
    url_regex = r'^create$'

    @utils.json_response
    def post(self, request):
	body = request.DATA
        print body


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
        for key in body['cephconfigkeys']:
            config = re.sub('\n', ';', body['cephconfig-{}'.format(key)])
            cephconfig.append(config)

        fiotest.gen_setup_ceph_config(dir_path, cephconfig)


        body['fiotypekeys'].append(1)
        body['bskeys'].append(1)
        body['iodepthkeys'].append(1)
        body['numjobkeys'].append(1)
        body['rwmixreadkeys'].append(1)

        for rwkey in body['fiotypekeys']:
            for bskey in body['bskeys']:
                for iodepthkey in body['iodepthkeys']:
                    for numjobkey in body['numjobkeys']:
                        for rwmixreadkey in body['rwmixreadkeys']:
                            fiotest.case(
                                dir_path,
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

        return "pass"

    @utils.json_response
    def options(self, request):
        return "option"

