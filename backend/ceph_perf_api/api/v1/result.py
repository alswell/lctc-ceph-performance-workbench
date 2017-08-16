# -*- coding: UTF-8 -*-
import urls
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
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.Result.objects.filter(**f).all()
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
