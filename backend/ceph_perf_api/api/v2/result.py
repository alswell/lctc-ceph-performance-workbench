# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models

    
@urls.register
class FIOTEST(generic.View):
    url_regex = r'^fiotest$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.Result.objects.filter(**f).all()
        for item in result:
            print item.jobid.time

        def foreign_convert(model):
            return "%s %s" % (model.jobid.name, model.jobid.time)

        d = utils.query_to_dict(result, "jobid", foreign_convert)
        return {"total": len(d), "data": d}


