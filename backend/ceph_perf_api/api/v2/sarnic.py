# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models


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
        return nodes


