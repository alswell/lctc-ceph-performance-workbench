# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils


DATA = {
    "iostat": {
        'wrqms': 'r*-',
        'avgrqsz': 'g*-',
        'r_await': 'b*-',
        'await': 'c*-',
        'ws': 'm*-',
        'avgqusz': 'y*-',
        'svctm': 'k*-',
        'rMBs': 'ro--',
        'wMBs': 'go--',
        'rrqms': 'bo--',
        'rs': 'co--',
        'tps': 'mo--',
        'util': 'yo--',
        'w_await': 'ko--',
    },
    "sarcpu": {
        'usr': 'r*-',
        'nice': 'g*-',
        'sys': 'b*-',
        'iowait': 'c*-',
        'steal': 'm*-',
        'irq': 'y*-',
        'soft': 'k*-',
        'guest': 'ro--',
        'gnice': 'go--',
        'idle': 'bo--',
    },
    "sarmem": {
        'kbmemfree': 'r*-',
        'kbmemused': 'g*-',
        'memused': 'b*-',
        'kbbuffers': 'c*-',
        'kbcached': 'm*-',
        'kbcommit': 'y*-',
        'commit': 'k*-',
        'kbactive': 'ro--',
        'kbinact': 'go--',
        'kbdirty': 'bo--',
    },
    "sarnic": {
        'rxpcks': 'r*-',
        'txpcks': 'g*-',
        'rxkBs': 'b*-',
        'txkBs': 'c*-',
        'rxcmps': 'm*-',
        'txcmps': 'y*-',
        'rxmcsts': 'k*-',
    },
}


@urls.register
class Dimension(generic.View):
    url_regex = r'^metric$'

    @utils.json_response
    def get(self, request):
        return DATA

