# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models


class JobConvert(utils.ForeignKeyConvert):
    def __init__(self):
        super(JobConvert, self).__init__("jobid")

    def __call__(self, model):
        return "%s %s" % (model.jobid.name, model.jobid.time)


def get_data(query_param):
    result = models.Result.objects.filter(**query_param).all()
    d = utils.query_to_dict(result, JobConvert())
    return d


KEYS = ['iodepth', 'numberjob', 'imagenum', 'clientnum']
KEY_MAP = {
    'iodepth': 'io',
    'numberjob': 'job',
    'imagenum': 'img',
    'clientnum': 'cli',
}


class FigureData(object):
    @staticmethod
    def jobs(d):
        dimension = {
            'iops': {},
            'lat': {},
            'bw': {},
        }

        x_label = {}
        for item in d:
            name = item['blocksize']
            for key in KEYS:
                name += '_%s%s' % (KEY_MAP.get(key, key), item[key])
            name += '_' + item['readwrite']
            x_label[name] = True

            for key, _ in dimension.items():
                try:
                    dimension[key][item['jobid']].update({name: item[key]})
                except KeyError:
                    dimension[key][item['jobid']] = {}
                    dimension[key][item['jobid']].update({name: item[key]})

        x_label = [k for k, v in x_label.items()]
        for key, _ in dimension.items():
            dimension[key]['name'] = x_label

        return dimension

    @staticmethod
    def jobs2(d):
        dimension = {
            'iops': {},
            'lat': {},
            'bw': {},
        }

        for item in d:
            name = item['blocksize']
            for key in KEYS:
                name += '_%s%s' % (KEY_MAP.get(key, key), item[key])
            name += '_' + item['readwrite']
            for key, _ in dimension.items():
                if not dimension[key].get(name):
                    dimension[key][name] = {}

            for key, _ in dimension.items():
                try:
                    dimension[key][name][item['jobid']] = item.get(key)
                except KeyError:
                    dimension[key][name][item['jobid']] = []
                    dimension[key][name][item['jobid']] = item.get(key)

        for key, value in dimension.items():
            items = value.items()
            items.sort()
            l = []
            for k, _ in items:
                dimension[key][k]['name'] = k
                l.append(dimension[key][k])
            dimension[key] = l

        return dimension

    @staticmethod
    def results(d):
        dimension = {
            'iops': [],
            'lat': [],
            'bw': [],
        }

        for item in d:
            for key, _ in dimension.items():
                dimension[key].append({'name': item.get('case_name'), key: item.get(key)})
        return dimension


@urls.register
class Figure(generic.View):
    url_regex = r'^figure$'

    @utils.json_response
    def get(self, request):
        """
        url examples:
        /api/v1/figure?type=results"         -d '{"id": [1,2,3,4,5,6,7]}'
        /api/v2/figure?type=jobs"            -d '{"jobid": [1,2,4,5,7]}'
        /api/v1/figure?type=jobs&version=2"  -d '{"jobid": [1,3,6,7]}'

        :param request:
        :return:
        """
        figure_type = request.GET.get('type')
        if figure_type:
            figure_type = figure_type[0]

        version = request.GET.get('version')
        if version:
            figure_type += version[0]

        d = get_data(utils.parse_filter_param(request.DATA))

        return getattr(FigureData, figure_type)(d)

