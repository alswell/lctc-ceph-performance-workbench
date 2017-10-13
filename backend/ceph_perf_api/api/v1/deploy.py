# -*- coding: UTF-8 -*-
import os
import sys
import urls
import yaml
import subprocess
import json
import re

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
class CLIENTS(generic.View):
    url_regex = r'^clients$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
        f = {}
        for key, value in dict(request.GET).items():
            f[key] = value[0]
        result = models.Cluster.objects.filter(**f).all()
        clients = utils.query_to_dict(result)[0]['clients'].split('\n')
        d = []
        for client in clients:
            d.append(client.split(":")[1])
        
        return d


@urls.register
class CLUSTERS(generic.View):
    url_regex = r'^cluster$'

    @utils.json_response
    def get(self, request):
        print dict(request.GET)
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
        cluster_info['clustername'] = body['clustername']
        cluster_info['public_network'] = body['publicnetwork']
        cluster_info['cluster_network'] = body['clusternetwork']
        cluster_info['objectstore'] = body['objectstore']
        if body.has_key('journalsize'):
            cluster_info['journal_size'] = body['journalsize']
        cluster_info['status'] = 'New'

        mons = []
        for mon in body['mon']:
            for key in body['nodeipkeys']:
                if body['node-{}'.format(key)] == mon:
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
            disk_list.append('{}:{}:{}'.format(
                body['node-{}'.format(key)],
                body['osddisk-{}'.format(key)],
                body['osdj-{}'.format(key)])
            )

        print cluster_info
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
        result = models.Cluster.objects.filter(id=id).all()
        d = utils.query_to_dict(result)

        if len(d) > 0:
            hwinfo_file = '{}/../../{}_ceph_hw_info.yml'.format(
                os.path.dirname(os.path.realpath(__file__)),
                id)
            with open(hwinfo_file, 'r') as f:
                ceph_info = yaml.load(f)
            client = ceph_info['ceph-client'].popitem()
            client_ip = client[1]['ip']
            client_password = client[1]['password']

            #update health
            try:
                cmd = "sshpass -p {} ssh -o StrictHostKeyChecking=no {} ceph health".format(client_password, client_ip)
                status = subprocess.check_output(cmd, shell=True)
            except Exception, e:
                body = {'health': ''}
            else:
                body = {'health': status}
                d[0]['health'] = status

            #update pool
            cmd = "sshpass -p {} ssh -o StrictHostKeyChecking=no {} 'ceph df -f json-pretty'".format(client_password, client_ip)
            pool = []
            try:
                output = subprocess.check_output(cmd, shell=True)
                output = json.loads(output)['pools']
                for item in output:
                    pool.append(item['name'])
            except Exception, e:
                pass
    
            d[0]['pools'] = pool
            body['pools'] = ','.join(pool)

            #update image
            image_output = ''
            images = []
            for p in pool:
                all_images = {}
                cmd = "sshpass -p {} ssh -o StrictHostKeyChecking=no {} 'rbd du --pool {}'".format(client_password, client_ip, p)
                try:
                    output = subprocess.check_output(cmd, shell=True)
                except Exception, e:
                    pass
                image_output = '{}pool: {}\n{}'.format(image_output, p, output)
                try:
                    status = output.split('\n')
                except Exception, e:
                    continue
                del status[0]
                del status[-1]
                if re.match('<TOTAL>', status[-1]):
                    del status[-1]
                print status
                for image_info in status:
                    match = re.match(r'([^\s]*)\s+([^\s]*)\s+([^\s]*)', image_info)
                    name_match = re.search('(.*)_(\d+)$', match.group(1))
                    if name_match:
                        image_name = name_match.group(1)
                        image_num = name_match.group(2)
                        size = match.group(2)
                        fill_size = match.group(3)
                        if size == fill_size:
                            if all_images.has_key(image_name):
                                all_images[image_name]['num'].append(image_num)
                            else:
                                all_images[image_name] = {'num': [image_num], 'size': size}
                for name, infos in all_images.items():
                   index = self.get_sequence_index(infos['num'])
                   images.append('{} {} {} {}'.format(name, infos['size'], index, p))
            body['images'] = ','.join(images)
            d[0]['image'] = image_output

            # update DB
            models.Cluster.objects.filter(id=id).update(**body)    
            return d[0]
        else:
            return []

    def get_sequence_index(self, mylist):
        mylist.sort()
        index = len(mylist)
        for item in mylist:
            if mylist.index(item) != int(item):
                index = mylist.index(item)
                break
        return index


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

