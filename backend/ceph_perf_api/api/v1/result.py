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
        result = models.Result.objects.all()
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}


@urls.register
class IoStat(generic.View):
    url_regex = r'^iostat/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.Iostat.objects.filter(caseid=caseid).all()
        d = utils.query_to_dict(result)
	nodes = {}
	for item in d:
	    key = "%s %s %s" % (item['node'], item['osdnum'], item['diskname'])
	    try:
	        nodes[key].append(item)
	    except KeyError:
	        nodes[key] = []
	        nodes[key].append(item)
        return {"total": len(d), "data": nodes}


@urls.register
class SarCPU(generic.View):
    url_regex = r'^sarcpu/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.SarCPU.objects.filter(caseid=caseid).all()
        d = utils.query_to_dict(result)
	nodes = {}
	for item in d:
	    try:
	        nodes[item['node']].append(item)
	    except KeyError:
	        nodes[item['node']] = []
	        nodes[item['node']].append(item)
        return {"total": len(d), "data": nodes}


@urls.register
class SarMem(generic.View):
    url_regex = r'^sarmem/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.SarMem.objects.filter(caseid=caseid).all()
        d = utils.query_to_dict(result)
	nodes = {}
	for item in d:
	    try:
	        nodes[item['node']].append(item)
	    except KeyError:
	        nodes[item['node']] = []
	        nodes[item['node']].append(item)
        return {"total": len(d), "data": nodes}


@urls.register
class SarNic(generic.View):
    url_regex = r'^sarnic/(?P<caseid>\d+)/$'

    @utils.json_response
    def get(self, request, caseid):
        result = models.SarNic.objects.filter(caseid=caseid).all()
        d = utils.query_to_dict(result)
	nodes = {}
	for item in d:
	    key = "%s %s" % (item['node'], item['network'])
	    try:
	        nodes[key].append(item)
	    except KeyError:
	        nodes[key] = []
	        nodes[key].append(item)
        return {"total": len(d), "data": nodes}


