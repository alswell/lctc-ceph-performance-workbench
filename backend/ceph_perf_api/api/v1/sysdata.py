# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils

DATA = {"data":
[
  {
    "id":"1",
    "key":"1",
    "caseid":"1",
    "node": "192.168.230.168",
    "time":"2017-08-02 13:33:56",
    "usr":"16",
    "nice":"0",
    "sys":"6",
    "iowait":"3",
    "steal":"0",
    "irq":"0",
    "soft":"0.5",
    "guest":"0",
    "gnice":"0",
    "idle":"74.5"
  },
],
"total":1
}

@urls.register
class SYSDATA(generic.View):
    url_regex = r'^sysdata$'

    @utils.json_response
    def get(self, request):
        return DATA

