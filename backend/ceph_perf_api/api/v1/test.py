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


def mk_data(data):
    d = {}
    d["sales"] = data
    return d

@urls.register
class Test(generic.View):
    url_regex = r'^dashboard$'

    @utils.json_response
    def get(self, request):
        name = [2008, 2009, 2010, 2011, 2012]
        cpu =  [1,    2,    3,    4,    5]
        mem =  [3,    2,    3,    4,    3]
        disk = [2,    4,    2,    1,    3]
        data = [2008, 2009, 2010, 2011, 2012]
        for i in range(len(name)):
            data[i] = {}
            data[i]["name"] = name[i]
            data[i]["cpu"] = cpu[i]
            data[i]["mem"] = mem[i]
            data[i]["disk"] = disk[i]

        return mk_data(data)

