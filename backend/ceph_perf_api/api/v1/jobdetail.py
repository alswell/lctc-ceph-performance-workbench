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
        jobdetail = {'numjob': [], 'fiotype': [], 'iodepth': [], 'rwmixread': []}

        jobid = dict(request.GET)['jobid'][0]
        result = models.Jobs.objects.filter(id=jobid).all()
        d = utils.query_to_dict(result)
        jobinfo = d[0]
        jobdetail['cluster'] = jobinfo['cluster']
        jobdetail['jobname'] = jobinfo['name']
        jobdetail['fiopara'] = jobinfo['fiopara']
        if jobinfo['ceph_config'] == 'default':
            jobdetail['cephconfig'] = ''
        else:
            jobdetail['cephconfig'] = jobinfo['ceph_config']

        if jobinfo['sysdata'] != None:
            sysdata = re.sub('[\[\]]', '', jobinfo['sysdata'])
            sysdata = re.sub('u\'', '', sysdata)
            sysdata = re.sub('\'', '', sysdata)

            jobdetail['sysdata'] = sysdata.split(', ')

        if jobinfo['testdir']:
            cmd = "ls {}/config".format(jobinfo['testdir'])
            cases = subprocess.check_output(cmd, shell=True).split('\n')
            del cases[-1]

            cmd = "grep rbdname {}/config/{}".format(jobinfo['testdir'], cases[0])
            imagename = subprocess.check_output(cmd, shell=True).split('=')[1].split('_')[0]
            if jobinfo['imagename'] != None and re.search(imagename, jobinfo['imagename']):
                jobdetail['imagename'] = jobinfo['imagename']
            else:
                jobdetail['imagename'] = ''
            
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
                i = 0
                while i < len(configs):
                    if re.match('%', configs[i]):
                        rwmixread = re.match('%(.*)', configs[i]).group(1)
                        if jobdetail['rwmixread'].count(rwmixread) == 0:
                            jobdetail['rwmixread'].append(rwmixread)
                    elif re.match('rw|randrw', configs[i]):
                        config = '{} {}'.format(configs[i], configs[i+1])
                        if jobdetail['fiotype'].count(config) == 0:
                            jobdetail['fiotype'].append(config)
                    elif re.match('iodepth', configs[i]):
                        iodepth = re.match('iodepth(.*)', configs[i]).group(1)
                        if jobdetail['iodepth'].count(iodepth) == 0:
                            jobdetail['iodepth'].append(iodepth)
                    elif re.match('numjob', configs[i]):
                        numjob = re.match('numjob(.*)', configs[i]).group(1)
                        if jobdetail['numjob'].count(numjob) == 0:
                            jobdetail['numjob'].append(numjob)
                    i = i + 1
            cmd = "cat {}/fioserver_list.conf".format(jobinfo['testdir'])
            jobdetail['clients'] = subprocess.check_output(cmd, shell=True).split('\n')
            del jobdetail['clients'][-1]

        return jobdetail
