import urllib
import json
from settings import HOST


def get_data_by_url(url):
    sock = urllib.urlopen(url)
    data = sock.read()
    sock.close()
    return json.loads(data)


def get_data(res, id=None):
    if id is not None:
        res += "/%s/" % id
    url = HOST + res
    return get_data_by_url(url)


def parse_data(data):
    all_data = {}
    for d in data:
        for k, v in d.items():
            try:
                all_data[k].append(v)
            except KeyError:
                all_data[k] = []
                all_data[k].append(v)
    return all_data


class FormatTime(object):
    def __init__(self, time_array):
        self.time_array = time_array

    def format_date(self, x, pos=None):
        if x < 0 or x >= len(self.time_array):
            return x
        if pos is None:
            return x

        if x - int(x) == 0:
            return self.time_array[int(x)]
        else:
            return ""

