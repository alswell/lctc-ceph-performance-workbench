from utils import get_data
from settings import LEGEND


def get_y_metric(use_local=True):
    if use_local:
        metric = {
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
            "sarnic" : {
                'rxpcks': 'r*-',
                'txpcks': 'g*-',
                'rxkBs': 'b*-',
                'txkBs': 'c*-',
                'rxcmps': 'm*-',
                'txcmps': 'y*-',
                'rxmcsts': 'k*-',
            },
         }
    else:
        metric = get_data('dimension')

    for key, value in metric.items():
        i = 0
        for m, legend in value.items():
            metric[key][m] = LEGEND[i]
            i += 1
    return metric


def query_result(result_filter):
    args = ""
    for key, value in result_filter.items():
        if value.get() != '':
            args += "&%s=%s" % (key, value.get())
    return get_data("fiotest" + args.replace('&', '?', 1))
