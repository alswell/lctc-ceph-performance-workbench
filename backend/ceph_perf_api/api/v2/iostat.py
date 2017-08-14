# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models


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
        return nodes


