# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from mysql import models
from job_conductor import api as job_api


@urls.register
class UserInfos(generic.View):
    url_regex = r'^userinfo$'

    @utils.json_response
    def get(self, request):
        result = models.UserInfo.objects.all()
        d = utils.query_to_dict(result)
        return {"value": d}

    @utils.json_response
    def post(self, request):
        body = request.DATA
        result = models.UserInfo.objects.create(**body)
        print result


@urls.register
class UserInfo(generic.View):
    url_regex = r'^userinfo/(?P<id>\d+)/$$'

    @utils.json_response
    def get(self, request, id):
        result = models.UserInfo.objects.filter(id=id).first()
        d = utils.query_to_dict(result)
        return {"value": d}

    @utils.json_response
    def delete(self, request, id):
        result = models.UserInfo.objects.filter(id=id).delete()

    @utils.json_response
    def put(self, request, id):
        body = request.DATA
        result = models.UserInfo.objects.filter(id=id).update(**body)


@urls.register
class Test(generic.View):
    url_regex = r'^testjob$'

    def __init__(self):
        self.job_conductor = job_api.API()

    @utils.json_response
    def post(self, request):
        body = request.DATA
        self.job_conductor.example_job(body)


