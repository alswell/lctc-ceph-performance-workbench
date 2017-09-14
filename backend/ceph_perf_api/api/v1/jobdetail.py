# -*- coding: UTF-8 -*-
import urls
import json
import os
import subprocess
import re

from django.views import generic
from ceph_perf_api import utils
from fiotest import models

@urls.register
class JOBDETAIL(generic.View):
    url_regex = r'^jobdetail$'

    @utils.json_response
    def get(self, request):
        jobdetail = {'numjob': [], 'bs': [], 'fiotype': [], 'iodepth': [], 'rwmixread': []}

        jobid = dict(request.GET)['jobid'][0]
        result = models.Jobs.objects.filter(id=jobid).all()
        d = utils.query_to_dict(result)
        jobinfo = d[0]
        jobdetail['cluster'] = jobinfo['cluster']
        jobdetail['jobname'] = jobinfo['name']
        jobdetail['fiopara'] = jobinfo['fiopara']
        jobdetail['cephconfig'] = jobinfo['ceph_config']
        print 

        cmd = "ls {}/config".format(jobinfo['testdir'])
        cases = subprocess.check_output(cmd, shell=True).split('\n')
        del cases[-1]
        #{u'clientkeys': [], u'client-1': u'192.168.230.199'}
        cmd = "grep rbdname {}/config/{}".format(jobinfo['testdir'], cases[0])
        jobdetail['imagename'] = subprocess.check_output(cmd, shell=True).split('=')[1].split('_')[0]
        

        onecase = cases[0].split('_')
        for config in onecase:
            pool_m = re.match('pool(.*)', config)
            if pool_m:
                jobdetail['poolname'] = pool_m.group(1)
        
            runtime_m = re.match('runtime(.*)', config)
            if runtime_m:
                jobdetail['runtime'] = runtime_m.group(1)

            imagenum_m = re.match('imagenum(.*)', config)
            if imagenum_m:
                jobdetail['imagecount'] = imagenum_m.group(1)

        for case in cases:
            configs = case.split('_')
            for config in configs:
                if re.match('\d+[kM]', config):
                    jobdetail['bs'].count(config)
                    if jobdetail['bs'].count(config) == 0:
                        jobdetail['bs'].append(config)
                elif re.match('%', config):
                    rwmixread = re.match('%(.*)', config).group(1)
                    jobdetail['rwmixread'].count(rwmixread)
                    if jobdetail['rwmixread'].count(rwmixread) == 0:
                        jobdetail['rwmixread'].append(rwmixread)
                elif re.match('rw|randrw', config):
                    jobdetail['fiotype'].count(config)
                    if jobdetail['fiotype'].count(config) == 0:
                        jobdetail['fiotype'].append(config)
                elif re.match('iodepth', config):
                    iodepth = re.match('iodepth(.*)', config).group(1)
                    jobdetail['iodepth'].count(iodepth)
                    if jobdetail['iodepth'].count(iodepth) == 0:
                        jobdetail['iodepth'].append(iodepth)
                elif re.match('numjob', config):
                    numjob = re.match('numjob(.*)', config).group(1)
                    jobdetail['numjob'].count(numjob)
                    if jobdetail['numjob'].count(numjob) == 0:
                        jobdetail['numjob'].append(numjob)


	cmd = "cat {}/fioserver_list.conf".format(jobinfo['testdir'])
        jobdetail['clients'] = subprocess.check_output(cmd, shell=True).split('\n')
        del jobdetail['clients'][-1]

        return jobdetail
