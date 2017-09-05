# -*- coding: UTF-8 -*-
import urls
from django.views import generic
from ceph_perf_api import utils
from ITuning_ceph_deploy import models
from job_conductor import api as job_api

@urls.register
class DeployCeph(generic.View):
    url_regex = r'^deploy$'


    def __init__(self):
        self.job_conductor = job_api.API()

    @utils.json_response
    def post(self, request):
        body = dict(request.DATA)
        print body
        #{u'osdj-1': u'/dev/sdc', u'osdj-3': u'/dev/sdc', u'osdj-2': u'/dev/sdc', u'nodepw-2': u'passw0rd', u'publicnetwork': u'192.168.230.0/24', u'nodepw-3': u'passw0rd', u'osddiskkeys': [1, 2, 3], u'nodeip-3': u'192.168.230.196', u'node-1': u'192.168.230.218', u'nodepw-1': u'passw0rd', u'node-3': u'192.168.230.196', u'node-2': u'192.168.230.201', u'nodekeys': [1, 2, 3], u'journalsize': u'10240', u'clusternetwork': u'192.168.220.0/24', u'clustername': u'test', u'nodepwkeys': [1, 2, 3], u'clientpwkeys': [1], u'objectstore': u'filestore', u'osddisk-3': u'/dev/sda', u'osddisk-2': u'/dev/sda', u'osddisk-1': u'/dev/sda', u'clientpw-1': u'passw0rd', u'clientip-1': u'192.168.230.199', u'osdjkeys': [1, 2, 3], u'nodeip-2': u'192.168.230.201', u'nodeip-1': u'192.168.230.218', u'nodeipkeys': [1, 2, 3], u'clientipkeys': [1], u'mon': [u'192.168.230.201']}


        cluster_info = {}
        cluster_info['name'] = body['clustername']
        cluster_info['public_network'] = body['publicnetwork']
        cluster_info['cluster_network'] = body['clusternetwork']
        cluster_info['objectstore'] = body['objectstore']
        cluster_info['journal_size'] = body['journalsize']
        cluster_info['mons'] = '\n'.join(body['mon'])
        cluster_info['status'] = 'New'

        osdhosts = []
        for key in body['nodeipkeys']:
            osdhosts.append(body['nodeip-{}'.format(key)])
        cluster_info['osdhosts'] = '\n'.join(osdhosts)

        clients = []
        for key in body['clientipkeys']:
            clients.append(body['clientip-{}'.format(key)])
        cluster_info['clients'] = '\n'.join(clients)

        result = models.Cluster.objects.create(**cluster_info)
        body['clusterid'] = result.id
        self.job_conductor.deploy(body)

        return "pass"

    @utils.json_response
    def options(self, request):
        return "option"


@urls.register
class CLUSTERS(generic.View):
    url_regex = r'^cluster$'

    @utils.json_response
    def get(self, request):
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        result = models.Cluster.objects.filter(**f).all().order_by('-id')
        d = utils.query_to_dict(result)
        return {"total": len(d), "data": d}

@urls.register
class CLUSTER(generic.View):
    url_regex = r'^cluster/(?P<id>\d+)/$'

    @utils.json_response
    def get(self, request, id):
        result = models.Cluster.objects.filter(id=id).all()
        d = utils.query_to_dict(result)
        if len(d) > 0:
            return d[0]
        else:
            return []


