# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from mysql import models

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

