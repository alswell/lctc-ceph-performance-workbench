# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from fiotest import models


class JobConvert(utils.ForeignKeyConvert):
    def __call__(self, model):
        return "%s %s" % (model.jobid.name, model.jobid.time)


@urls.register
class FIOTEST(generic.View):
    url_regex = r'^fiotest$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        print f
        result = models.Result.objects.filter(**f).all()

        d = utils.query_to_dict(result, JobConvert("jobid"))
        return {"total": len(d), "data": d}


def mk_check(n, array):
    check = []
    for i in range(n):
        check.append(False)
    for i in array:
        check[i] = True
    return check


def jobs(array):
    result = models.Result.objects.all()
    d = utils.query_to_dict(result, JobConvert("jobid"))
    total = len(d)
    check = mk_check(total, array)

    dimension = {
        'iops': {},
        'lat': {},
        'bw': {},
    }

    x_label = {}
    keys = ['iodepth', 'numberjob', 'imagenum', 'clientnum']
    for item in [d[i] for i in range(total) if check[i]]:
        name = item['blocksize']
        for key in keys:
            name += '_%s%s' % (key, item[key])
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


def jobs2(array):
    result = models.Result.objects.all()
    d = utils.query_to_dict(result, JobConvert("jobid"))
    total = len(d)
    check = mk_check(total, array)

    dimension = {
        'iops': {},
        'lat': {},
        'bw': {},
    }

    keys = ['iodepth', 'numberjob', 'imagenum', 'clientnum']
    for item in [d[i] for i in range(total) if check[i]]:
        name = item['blocksize']
        for key in keys:
            name += '_%s%s' % (key, item[key])
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


def results(array):
    result = models.Result.objects.all()
    d = utils.query_to_dict(result, JobConvert("jobid"))
    total = len(d)
    check = mk_check(total, array)

    dimension = {
        'iops': [],
        'lat': [],
        'bw': [],
    }

    for item in [d[i] for i in range(total) if check[i]]:
        for key, _ in dimension.items():
            dimension[key].append({'name': item.get('case_name'), key: item.get(key)})
    return dimension


@urls.register
class Figure(generic.View):
    url_regex = r'^figure$'

    @utils.json_response
    def get(self, request):
        body = request.DATA
        print body
        type = body['type']
        array = body['id']
        if type == "job":
            return jobs(array)
        elif type == "result":
            return results(array)

