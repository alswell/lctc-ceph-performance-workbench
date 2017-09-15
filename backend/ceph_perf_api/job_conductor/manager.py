import time
import os
import sys
import re
import json
import yaml
import datetime


file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_path, ".."))
from fiotest.fio_test import run_suite
from fiotest.fio_test import init_image
from ITuning_ceph_deploy.ITuning_ceph_deploy import ceph_deploy
from ITuning_ceph_deploy.ITuning_ceph_deploy import todb as clusterdb
from oslo_log import log as logging
LOG = logging.getLogger(__name__)


class Manager(object):
    def example_job(self, ctxt, body):
        LOG.info("run example, body: %s", body)
        print "run example, body:", body
        for i in range(10):
            LOG.info("doing ... (%s)", i)
            time.sleep(1)
        print "done!"

    def run_fio(self, ctxt, body):
        LOG.info("run fio: %s", body)
        try:
            runfio = run_suite.RunFIO(body['suite_dir'], body['cluster'])
            if body.has_key('ceph_config'):
                log_dir = runfio.run(
                    body['jobname'],
                    body['jobid'],
                    ceph_config=body['ceph_config'],
                    sysdata=body['sysdata']
                )
            else:
                log_dir = runfio.run(
                    body['jobname'],
                    body['jobid'],
                    sysdata=body['sysdata']
                ) 
        except Exception, e:
            print e
            runfio = run_suite.RunFIO(body['suite_dir'], body['cluster'])
            job_status = runfio.fiodb.query_jobs(body['jobid'])[0][3]
            if job_status != "Canceled":
                error_info = re.sub("u'", '', str(e))
                error_info = re.sub("'", '', str(e))
                jobinfo = {'status': "Failed: {}".format(error_info)}
                runfio.fiodb.update_jobs(body['jobid'], **jobinfo)
            if body.has_key('ceph_config'):
                runfio.set_default_ceph_config(body['ceph_config'])
        else:
            runfio.store_logfile_FS(log_dir)
            print "finish"

    def deploy(self, ctxt, body):
        LOG.info("deploy ceph: %s", body)

        deploy = ceph_deploy.Deploy()
        hwinfo_file = '{}/../{}_ceph_hw_info.yml'.format(
            os.path.dirname(os.path.realpath(__file__)),
            body['id'])
        with open(hwinfo_file, 'r') as f:
            ceph_info = yaml.load(f)

        osdhost_list = []
        nodepw_list = []
        nodeips = []
        disk_list = []
        for node, data in ceph_info['ceph-node'].items():
            osdhost_list.append(node)
            nodepw_list.append(data['password'])
            nodeips.append(data['ip'])
            for osd, osddata in data['osd'].items():
                disk_list.append('{}:{}:{}'.format(
                    node,
                    osddata['osd-disk'],
                    osddata['journal-disk'],
                ))

        client_list = []
        clientpw_list = []
        clientips = []
        for key, value in ceph_info['ceph-client'].items():
            client_list.append(key)
            clientpw_list.append(value['password'])
            clientips.append(value['ip'])

        ips = nodeips + clientips
        hostnames = osdhost_list + client_list
        password = nodepw_list + clientpw_list

        mon_list = []
        mons = body['mons'].split("\n")
        for mon in mons:
            mon_list.append(mon.split(':')[0]) 

        name = body["name"]
        public_network = body['public_network']
        cluster_network = body['cluster_network']
        objectstore = body['objectstore']
        journal_size = body['journal_size']


        with open('/tmp/ITuning_ceph.conf', 'w') as f:
            f.write('[global]\n')
            f.write('public_network = {}\n'.format(public_network))
            f.write('cluster_network = {}\n'.format(cluster_network))
            f.write('osd objectstore = {}\n'.format(objectstore))
            f.write('[osd]\n')
            f.write('osd journal size = {}\n'.format(journal_size))

        conf = '/tmp/ITuning_ceph.conf'
        try:
            print datetime.datetime.now(), "init" 
            for i in range(len(ips)):
                deploy.initenv(body['id'], ips[i], password[i], hostnames[i])
            print datetime.datetime.now(), "purge" 
            deploy.purge(body['id'], name, hostnames)
            print datetime.datetime.now(), "deploy" 
            deploy.deploy(body['id'], name, mon_list, osdhost_list, disk_list, client_list, conf)
            print datetime.datetime.now(), "create pool" 
            deploy.createrbdpool(len(disk_list), mon_list[0])
            print datetime.datetime.now(), "get default ceph config" 
            deploy.get_default_cephconfig(body['id'], mon_list[0], password=None)
            for client in client_list:
                print datetime.datetime.now(), "install fio in {}".format(client)
                deploy.install_fio(client)
            for host in hostnames:
                print datetime.datetime.now(), "reboot {}".format(host)
                deploy.reboot(host)
            for client in client_list:
                print datetime.datetime.now(), "check and start fio server in {}".format(host)
                deploy.checkandstart_fioser(client)
        except Exception, e:
            db = clusterdb.ToDB()
            error_info = re.sub("u'", '', str(e))
            error_info = re.sub("'", '', str(e))
            cinfo = {'status': "Failed: {}".format(error_info)}
            db.update_cluster(body['id'], **cinfo)
            print e
        else:
            print "finish"

    def initimage(self, ctxt, body):
        LOG.info("deploy ceph: %s", body)
        print body
        hwinfo_file = '{}/../{}_ceph_hw_info.yml'.format(
            os.path.dirname(os.path.realpath(__file__)),
            body['clusterid'])
        with open(hwinfo_file, 'r') as f:
            ceph_info = yaml.load(f)
        client_name, client_data = ceph_info['ceph-client'].popitem()
        client_ip = client_data['ip']
        client_password = client_data['password']

        print datetime.datetime.now(), "gen fullfill file"
        file_dir = init_image.fullfill_file(body['imagename'], body['imagesize'], body['imagenum'], body['pool'])

        print datetime.datetime.now(), "create image"
        init_image.create_image(body['imagename'], body['imagesize'], body['imagenum'], body['pool'], client_ip, client_password)
        print datetime.datetime.now(),"full fill"
        init_image.fullfill(file_dir, body['imagename'], body['imagesize'], client_ip, client_password)
        print "finish"

