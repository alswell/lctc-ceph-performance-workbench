# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils

DATA = {
    "iostat": {
    'wMBs': 'mx-',
    'tps': 'y*-',
    'avgrqsz': 'co-',
    },
    "sarcpu": {
    'iowait': 'mx-',
    'irq': 'y*-',
    'soft': 'co-',
    },
}

@urls.register
class Dimension(generic.View):
    url_regex = r'^dimension$'

    @utils.json_response
    def get(self, request):
        return DATA

