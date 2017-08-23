# -*- coding: UTF-8 -*-
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
        if len(dict(request.GET)) > 0:
            output = {}
            for key, values in dict(request.GET).items():
                for value in values:
                    f[key] = value
                    r = models.Result.objects.filter(**f).all()
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
                        if output.has_key(case_name):
                            output[case_name]['{}_iops'.format(value)] = result['iops']
                            output[case_name]['{}_lat'.format(value)] = result['lat']
                            output[case_name]['{}_bw'.format(value)] = result['bw']
                        else:
                            output[case_name] = {}
                            output[case_name]['{}_iops'.format(value)] = result['iops']
                            output[case_name]['{}_lat'.format(value)] = result['lat']
                            output[case_name]['{}_bw'.format(value)] = result['bw']
            d = []
            for key, value in output.items():
                tmp_dic = {'casename': key}
                tmp_dic.update(value)
                d.append(tmp_dic)
            return d
        else:
            result = models.Result.objects.filter(jobid=jobid).all()
            d = utils.query_to_dict(result)
            return {"total": len(d), "data": d}

@urls.register
class FIOTEST(generic.View):
    url_regex = r'^fiotest/(?P<jobid>\d+)/$'

    @utils.json_response
    def get(self, request, jobid):
        result = models.Result.objects.filter(jobid=jobid).all()
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
