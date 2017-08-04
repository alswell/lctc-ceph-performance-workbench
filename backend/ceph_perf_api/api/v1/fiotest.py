# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils

DATA = {"data":
[
  {
    "id":"1",
    "key":"1",
    "case_name":"rbd_rw_4k_runtime10_iodepth1_numjob1_imagenum1_test1_%50_2017_08_02_13_33_52",
    "time":"2017-08-02 13:33:52",
    "blocksize":"4k",
    "iodepth":1,
    "numberjob":1,
    "imagenum":1,
    "clientnum":1,
    "readwrite":"rw%50",
    "iops":72,
    "lat":22.43,
    "sysdata":"sysdata",
  },
],
"total":1
}
    
@urls.register
class FIOTEST(generic.View):
    url_regex = r'^fiotest$'

    @utils.json_response
    def get(self, request):
        return DATA

