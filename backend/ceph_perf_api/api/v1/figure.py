# -*- coding: UTF-8 -*-
import copy
import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models


class JobConvert(utils.ForeignKeyConvert):
    def __init__(self):
        super(JobConvert, self).__init__("jobid")

    def __call__(self, model):
        return "%s %s" % (model.jobid.name, model.jobid.time)


KEYS = ['iodepth', 'numberjob', 'imagenum', 'clientnum']
KEY_MAP = {
    'iodepth': 'io',
    'numberjob': 'job',
    'imagenum': 'img',
    'clientnum': 'cli',
}
DIMENSION = [
    'r_iops',
    'w_iops',
    'iops',
    'lat',
    'bw',
    'r_bw',
    'w_bw',
]


class FigureData(object):
    @staticmethod
    def _mk_dims(e={}):
        dims = {}
        for dim in DIMENSION:
            dims[dim] = copy.copy(e)
        return dims

    @staticmethod
    def _mk_name(item):
        name = item['blocksize']
        for key in KEYS:
            name += '_%s%s' % (KEY_MAP.get(key, key), item[key])
        name += '_' + item['readwrite']
        return name

    @classmethod
    def jobs(cls, d):
        dims = cls._mk_dims()

        x_label = {}
        for item in d:
            name = cls._mk_name(item)
            x_label[name] = True

            for key, _ in dims.items():
                job_id = item['jobid']
                if not dims[key].get(job_id):
                    dims[key][job_id] = {}
                dims[key][job_id][name] = item[key]

        x_label = [k for k, v in x_label.items()]
        for key, _ in dims.items():
            dims[key]['name'] = x_label

        return dims

    @classmethod
    def jobs2(cls, d):
        dims = cls._mk_dims()

        for item in d:
            name = cls._mk_name(item)
            for key, _ in dims.items():
                if not dims[key].get(name):
                    dims[key][name] = {}

            for key, _ in dims.items():
                dims[key][name][item['jobid']] = item.get(key)

        for key, value in dims.items():
            items = value.items()
            items.sort()
            l = []
            for k, _ in items:
                dims[key][k]['name'] = k
                l.append(dims[key][k])
            dims[key] = l

        return dims

    @classmethod
    def results(cls, d):
        dims = cls._mk_dims([])

        for item in d:
            for key, _ in dims.items():
                dims[key].append({'name': item.get('case_name'), key: item.get(key)})
        return dims

    @staticmethod
    def results2(d):
        l = []
        for item in d:
            one = {'name': item.get('case_name')}
            for key in DIMENSION:
                one[key] = item.get(key)
            l.append(one)
        return {'value': l}


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

        query_param = utils.parse_filter_param(request.DATA)
        result = models.Result.objects.filter(**query_param).all()
        d = utils.query_to_dict(result, JobConvert())

        return getattr(FigureData, figure_type)(d)

