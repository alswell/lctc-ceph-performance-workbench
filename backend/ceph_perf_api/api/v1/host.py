# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils

DATA = {"data":
[
{"id":"476718466","key":"965782434","name":"Carol Miller","nickName":"Perez","phone":"13097464770","age":49,"address":"陕西省 咸阳市 渭城区","isMale":1,"email":"m.eibloooimw@gvfatp.tw","createTime":"2008-12-26 00:09:59","avatar":"http://dummyimage.com/100x100/dd79f2/757575.png&text=P"},
{"id":"136003323","key":"988829554","name":"Amy Johnson","nickName":"Miller","phone":"15839615675","age":91,"address":"河北省 沧州市 河间市","isMale":1,"email":"p.yhyaiod@yklcs.es","createTime":"2004-09-01 02:44:05","avatar":"http://dummyimage.com/100x100/79f2b9/757575.png&text=M"},
{"id":"821244493","key":"342517141","name":"Daniel Lopez","nickName":"Moore","phone":"15258174840","age":92,"address":"河南省 鹤壁市 山城区","isMale":1,"email":"l.oxstzt@wxuge.tr","createTime":"1972-09-25 10:05:23","avatar":"http://dummyimage.com/100x100/f29679/757575.png&text=M"}
],
"total":3
}
    
@urls.register
class Hosts(generic.View):
    url_regex = r'^host$'

    @utils.json_response
    def get(self, request):
        return DATA

@urls.register
class Host(generic.View):
    url_regex = r'^host/(?P<id>\d+)/$$'

    @utils.json_response
    def get(self, request, id):
        return DATA["data"][int(id)]
