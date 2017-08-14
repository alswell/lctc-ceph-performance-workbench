# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models


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
        return nodes


