# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models

@urls.register
class HWINFOS(generic.View):
    url_regex = r'^hwinfo$'

    @utils.json_response
    def get(self, request):
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]

        result = models.HWInfo.objects.filter(**f).all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class HWINFO(generic.View):
    url_regex = r'^hwinfo/(?P<jobid>\d+)/$'

    @utils.json_response
    def get(self, request, jobid):
        result = models.HWInfo.objects.filter(jobid=jobid).all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class OSINFOS(generic.View):
    url_regex = r'^osinfo$'

    @utils.json_response
    def get(self, request):
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]

        result = models.OSInfo.objects.filter(**f).all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class OSINFO(generic.View):
    url_regex = r'^osinfo/(?P<jobid>\d+)/$'

    @utils.json_response
    def get(self, request, jobid):
        result = models.OSInfo.objects.filter(jobid=jobid).all()
        d = utils.query_to_dict(result)

        return {"total": len(d), "data": d}

@urls.register
class DISKINFOS(generic.View):
    url_regex = r'^diskinfo$'

    @utils.json_response
    def get(self, request):
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        result = models.DiskInfo.objects.filter(**f).all()
        d = utils.query_to_dict(result)

        return {"total": len(d), "data": d}

@urls.register
class DISKINFO(generic.View):
    url_regex = r'^diskinfo/(?P<jobid>\d+)/$'

    @utils.json_response
    def get(self, request, jobid):
        result = models.DiskInfo.objects.filter(jobid=jobid).all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}


@urls.register
class CephConfigs(generic.View):
    url_regex = r'^cephconfig$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.CephConfig.objects.filter(**f).all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class CephConfig(generic.View):
    url_regex = r'^cephconfig/(?P<jobid>\d+)/$'

    @utils.json_response
    def get(self, request, jobid):
        result = models.CephConfig.objects.filter(jobid=jobid).all()
        d = utils.query_to_dict(result)
        #return {"total": len(d), "data": d}
        if len(d) > 0:
            return d[0]
        else:
            return []

