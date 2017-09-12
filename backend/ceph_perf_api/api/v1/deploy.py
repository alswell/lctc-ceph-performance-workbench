# -*- coding: UTF-8 -*-
import os
import sys
import urls
import yaml
import subprocess
import json

from django.views import generic
from ceph_perf_api import utils
from ITuning_ceph_deploy import models
from ITuning_ceph_deploy.ITuning_ceph_deploy import ceph_deploy
from job_conductor import api as job_api

@urls.register
class DeployCeph(generic.View):
    url_regex = r'^deploy$'


    def __init__(self):
        self.job_conductor = job_api.API()

    @utils.json_response
    def options(self, request):
        return "option"

    @utils.json_response
    def post(self, request):
        body = dict(request.DATA)
        print body
        self.job_conductor.deploy(body)

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

    @utils.json_response
    def delete(self, request):
        id = dict(request.DATA)['id']
        result = models.Cluster.objects.filter(id=id).all()[0]
        result.delete()
        hwinfo_file = '{}/../../{}_ceph_hw_info.yml'.format(
            os.path.dirname(os.path.realpath(__file__)),
            id)
        subprocess.call('rm -f {}'.format(hwinfo_file), shell=True)
        
        return "delete Failed job {}".format(id)

    @utils.json_response
    def options(self, request):
        return "option"

    @utils.json_response
    def post(self, request):
        body = dict(request.DATA)
        print body

        deploy = ceph_deploy.Deploy()
        cluster_info = {}
        cluster_info['name'] = body['clustername']
        cluster_info['public_network'] = body['publicnetwork']
        cluster_info['cluster_network'] = body['clusternetwork']
        cluster_info['objectstore'] = body['objectstore']
        cluster_info['journal_size'] = body['journalsize']
        cluster_info['status'] = 'New'

        mons = []
        for mon in body['mon']:
            for key in body['nodeipkeys']:
                if body['nodeip-{}'.format(key)] == mon:
                    mons.append('{}:{}'.format(body['nodename-{}'.format(key)], body['nodeip-{}'.format(key)]))
        cluster_info['mons'] = '\n'.join(mons)

        osdhosts = []
        osdhost_list = []
        nodeips = []
        nodepw_list = []
        for key in body['nodeipkeys']:
            osdhosts.append('{}:{}'.format(body['nodename-{}'.format(key)], body['nodeip-{}'.format(key)]))
            osdhost_list.append(body['nodename-{}'.format(key)])
            nodeips.append(body['nodeip-{}'.format(key)])
            nodepw_list.append(body['nodepw-{}'.format(key)])
        cluster_info['osdhosts'] = '\n'.join(osdhosts)

        clients = []
        clientpw_list = []
        client_list = []
        clientips = []
        for key in body['clientipkeys']:
            clients.append('{}:{}'.format(body['clientname-{}'.format(key)], body['clientip-{}'.format(key)]))
            client_list.append(body['clientname-{}'.format(key)])
            clientips.append(body['clientip-{}'.format(key)])
            clientpw_list.append(body['clientpw-{}'.format(key)])
        cluster_info['clients'] = '\n'.join(clients)

        ips = nodeips + clientips
        disk_list = []
        for key in body['nodekeys']:
            i = ips.index(body['node-{}'.format(key)])
            disk_list.append('{}:{}:{}'.format(
                osdhost_list[i],
                body['osddisk-{}'.format(key)],
                body['osdj-{}'.format(key)])
            )

        result = models.Cluster.objects.create(**cluster_info)
        clusterid = result.id

        deploy.gen_yaml_file(
            clusterid,
            disk_list,
            osdhost_list,
            nodeips,
            nodepw_list,
            client_list,
            clientips,
            clientpw_list,
            body['publicnetwork'],
            body['clusternetwork'],
        )

        cmd = "sshpass -p {} ssh {} 'ls /etc/ceph/ceph.conf /usr/bin/ceph'".format(nodepw_list[0], nodeips[0])
        try:
            subprocess.check_call(cmd, shell=True)
        except Exception:
            pass
        else: 
            deploy.get_default_cephconfig(
                clusterid, nodeips[0], password=nodepw_list[0])

        return "pass"

@urls.register
class CLUSTER(generic.View):
    url_regex = r'^cluster/(?P<id>\d+)/$'

    @utils.json_response
    def get(self, request, id):
        hwinfo_file = '{}/../../{}_ceph_hw_info.yml'.format(
            os.path.dirname(os.path.realpath(__file__)),
            id)
        with open(hwinfo_file, 'r') as f:
            ceph_info = yaml.load(f)
        client = ceph_info['ceph-client'].popitem()
        client_ip = client[1]['ip']
        client_password = client[1]['password']
        try:
            cmd = "sshpass -p {} ssh -o StrictHostKeyChecking=no {} ceph health".format(client_password, client_ip)
            status = subprocess.check_output(cmd, shell=True)
        except Exception, e:
            body = {'health': ''}
        else:
            body = {'health': status}
            models.Cluster.objects.filter(id=id).update(**body)

        result = models.Cluster.objects.filter(id=id).all()
        d = utils.query_to_dict(result)

        cmd = "sshpass -p {} ssh -o StrictHostKeyChecking=no {} 'rbd du'".format(client_password, client_ip)
        try:
            image = subprocess.check_output(cmd, shell=True)
        except Exception, e:
            image = ''

        if len(d) > 0:
            d[0]['image'] = image
            return d[0]
        else:
            return []

@urls.register
class DEFAULTCEPHCONFIG(generic.View):
    url_regex = r'^defaultcephconfig/(?P<clusterid>\d+)/$'

    @utils.json_response
    def get(self, request, clusterid):
        result = models.DefaultCephConfig.objects.filter(clusterid=clusterid).all()
        d = utils.query_to_dict(result)
        if len(d) > 0:
            return json.loads(d[-1]['total'])
            #return d[0]
        else:
            return []

@urls.register
class DEFAULTCEPHCONFIG(generic.View):
    url_regex = r'^defaultcephconfig$'

    @utils.json_response

    def post(self, request):
        body = dict(request.DATA)

        deploy = ceph_deploy.Deploy()
        hwinfo_file = '{}/../../{}_ceph_hw_info.yml'.format(
            os.path.dirname(os.path.realpath(__file__)),
            body['id'])
        with open(hwinfo_file, 'r') as f:
            ceph_info = yaml.load(f)

        node, data = ceph_info['ceph-node'].popitem()
        deploy.get_default_cephconfig(body['id'], data['ip'], data['password'])

        return 'pass'

    @utils.json_response
    def options(self, request):
        return "option"

