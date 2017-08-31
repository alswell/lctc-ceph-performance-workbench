# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from ITuning_ceph_deploy import models
from job_conductor import api as job_api

@urls.register
class DeployCeph(generic.View):
    url_regex = r'^deploy$'


    def __init__(self):
        self.job_conductor = job_api.API()

    @utils.json_response
    def post(self, request):
        body = request.DATA

        result = models.Cluster.objects.create(**body)
        body['clusterid'] = result.id
        self.job_conductor.deploy(body)

        return "pass"

    @utils.json_response
    def options(self, request):
        return "option"


@urls.register
class CLUSTERS(generic.View):
    url_regex = r'^cluster$'

    @utils.json_response
    def get(self, request):
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        result = models.Cluster.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

