# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models

@urls.register
class SARCPUS(generic.View):
    url_regex = r'^sarcpu$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.SarCPU.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class SARCPU(generic.View):
    url_regex = r'^sarcpu/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.SarCPU.objects.filter(caseid=caseid).all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class SARMEMS(generic.View):
    url_regex = r'^sarmem$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.SarMem.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class SARMEM(generic.View):
    url_regex = r'^sarmem/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.SarMem.objects.filter(caseid=caseid).all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class SARNICS(generic.View):
    url_regex = r'^sarnic$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.SarNic.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class SARNIC(generic.View):
    url_regex = r'^sarnic/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.SarNic.objects.filter(caseid=caseid).all().order_by('network')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class Iostats(generic.View):
    url_regex = r'^iostat$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.Iostat.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class Iostat(generic.View):
    url_regex = r'^iostat/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.Iostat.objects.filter(caseid=caseid).all().order_by('osdnum')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class CephStatuss(generic.View):
    url_regex = r'^cephstatus$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.CephStatus.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class CephStatus(generic.View):
    url_regex = r'^cephstatus/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.CephStatus.objects.filter(caseid=caseid).all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class CephInfos(generic.View):
    url_regex = r'^cephinfo$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.CephInfo.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class CephInfo(generic.View):
    url_regex = r'^cephinfo/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.CephInfo.objects.filter(caseid=caseid).all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class CephPoolInfos(generic.View):
    url_regex = r'^poolinfo$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.CephPoolInfo.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class CephPoolInfo(generic.View):
    url_regex = r'^poolinfo/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.CephPoolInfo.objects.filter(caseid=caseid).all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class PerfDumps(generic.View):
    url_regex = r'^perfdump$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.PerfDump.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class PerfDump(generic.View):
    url_regex = r'^perfdump/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.PerfDump.objects.filter(caseid=caseid).all()
        d = utils.query_to_dict(result)
        #return {"total": len(d), "data": d}
        return d
