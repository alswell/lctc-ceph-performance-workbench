# -*- coding: UTF-8 -*-
import subprocess
import urls
import re
from django.views import generic
from ceph_perf_api import utils
from fiotest import models

    
@urls.register
class FIOTESTS(generic.View):
    url_regex = r'^fiotest$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        if len(dict(request.GET)) == 1 and dict(request.GET).has_key('jobid'):
            output = {}
            for key, values in dict(request.GET).items():
                for value in values:
                    f[key] = value
                    r = models.Result.objects.filter(**f).all().order_by(
                        'jobid', 'blocksize', 'imagenum', 'readwrite', 'numberjob', 'iodepth')
                    results = utils.query_to_dict(r)
                    for result in results:
                        case_name = '{}_{}_{}_{}_{}_{}'.format(
                            result['blocksize'],
                            result['iodepth'],
                            result['numberjob'],
                            result['imagenum'],
                            result['clientnum'],
                            result['readwrite']
                        )
                        j = {}
                        j['id'] = value
                        job_r = models.Jobs.objects.filter(**j).all()
                        result_j = utils.query_to_dict(job_r)[0]
                        if output.has_key(case_name):
                            output[case_name]['{}_iops'.format(value)] = result['iops']
                            output[case_name]['{}_lat'.format(value)] = result['lat']
                            output[case_name]['{}_bw'.format(value)] = result['bw']
                            if result_j.has_key('name'):
                                output[case_name]['{}{}_iops'.format(value, result_j['name'])] = result['iops']
                                output[case_name]['{}{}_lat'.format(value, result_j['name'])] = result['lat']
                                output[case_name]['{}{}_bw'.format(value, result_j['name'])] = result['bw']
                        else:
                            output[case_name] = {}
                            output[case_name]['{}_iops'.format(value)] = result['iops']
                            output[case_name]['{}_lat'.format(value)] = result['lat']
                            output[case_name]['{}_bw'.format(value)] = result['bw']
                            if result_j.has_key('name'):
                                output[case_name]['{}{}_iops'.format(value, result_j['name'])] = result['iops']
                                output[case_name]['{}{}_lat'.format(value, result_j['name'])] = result['lat']
                                output[case_name]['{}{}_bw'.format(value, result_j['name'])] = result['bw']
            d = []
            for key, value in output.items():
                tmp_dic = {'casename': key}
                tmp_dic.update(value)
                d.append(tmp_dic)
            return d

        else:
            filter_param = utils.parse_filter_param(request.DATA, request.GET)
            result = models.Result.objects.filter(**filter_param).all().order_by('-jobid',
                'blocksize', 'imagenum', 'readwrite', 'numberjob', 'iodepth')
            d = utils.query_to_dict(result)
            return {"total": len(d), "data": d}

@urls.register
class FIOTEST(generic.View):
    url_regex = r'^fiotest/(?P<jobid>\d+)/$'

    @utils.json_response
    def get(self, request, jobid):
        result = models.Result.objects.filter(jobid=jobid).all().order_by(
            'blocksize', 'imagenum', 'readwrite', 'numberjob', 'iodepth')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}


@urls.register
class FIOJOBS(generic.View):
    url_regex = r'^fiojobs$'

    @utils.json_response
    def get(self, request):
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        result = models.Jobs.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

    @utils.json_response
    def options(self, request):
        return "option"

    @utils.json_response
    def put(self, request):
        body = {}
        for key, value in dict(request.DATA).items():
            if key == 'id':
                jobid = value
            else:
                body[key] = value
        
        result = models.Jobs.objects.filter(id=jobid).all()[0]
        if result.status == "New":
            body = {'status': 'Canceled'}
            models.Jobs.objects.filter(id=jobid).update(**body)
            return "pass"
        if result.status != "Finished":
            models.Jobs.objects.filter(id=jobid).update(**body)
            return "pass"
        else:
            raise Exception("Error: The Finished job can't be Cancel!")


    @utils.json_response
    def delete(self, request):
        jobid = dict(request.DATA)['id']
        result = models.Jobs.objects.filter(id=jobid).all()[0]
        if re.match("Failed", result.status):
            result.delete()
        elif result.status == "Canceled":
            result.delete()
        elif result.status == "Finished":
            result.delete()
        else:
            raise Exception("Error: The job with status {} can't be deleted!".format(result.status))
        if result.testdir:
            cmd = "rm -rf {}".format(result.testdir)
            subprocess.check_call(cmd, shell=True)
        return "delete {} job {}".format(result.status, jobid)
