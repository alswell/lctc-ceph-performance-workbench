import time
import os
import sys
import re
import json


file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_path, ".."))
from fiotest.fio_test import run_suite
from ITuning_ceph_deploy.ITuning_ceph_deploy import ceph_deploy
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
            runfio = run_suite.RunFIO(body['suite_dir'], todb=True)
            if body.has_key('ceph_config'):
                log_dir = runfio.run(
                    body['suite_dir'],
                    body['jobname'],
                    body['jobid'],
                    ceph_config=body['ceph_config']
                )
            else:
                log_dir = runfio.run(
                    body['suite_dir'],
                    body['jobname'],
                    body['jobid']
                ) 
        except Exception, e:
            runfio = run_suite.RunFIO(body['suite_dir'], todb=True)
            job_status = runfio.db.query_jobs(body['jobid'])[0][3]
            if job_status != "Canceled":
                error_info = re.sub("'", '', e)
                error_info = re.sub('"', '', error_info)
                jobinfo = {'status': "Failed: {}".format(e)}
                runfio.db.update_jobs(body['jobid'], **jobinfo)
            print e
        else:
            runfio.store_logfile_FS(log_dir)
            print "finish"

    def deploy(self, ctxt, body):
        LOG.info("deploy ceph: %s", body)
        name = body["clustername"]

        osdhost_list = []
        client_list = []
        for i in range(len(body['nodeipkeys'])):
            osdhost_list.append('ceph-{}'.format(str(i+1)))

        for i in range(len(body['clientipkeys'])):
            client_list.append('client-{}'.format(str(i+1)))

        ips = []
        for key in body['nodeipkeys']:
            ips.append(body['nodeip-{}'.format(key)])
        for key in body['clientipkeys']:
            ips.append(body['clientip-{}'.format(key)])
        password = 'passw0rd'

        mon_list = []
        for mon in body['mon']:
            i = ips.index(mon)
            mon_list.append(osdhost_list[i]) 

        disk_list = []
        for key in body['nodekeys']:
            print key
            i = ips.index(body['node-{}'.format(key)])
            print osdhost_list
            print i
            print body['node-{}'.format(key)]
            print body['osddisk-{}'.format(key)], body['osdj-{}'.format(key)]
            disk_list.append('{}:{}:{}'.format(osdhost_list[i], body['osddisk-{}'.format(key)], body['osdj-{}'.format(key)]))

        hostnames = osdhost_list + client_list
    
        public_network = body['publicnetwork']
        cluster_network = body['clusternetwork']
        objectstore = body['objectstore']
        journal_size = body['journalsize']

        with open('/tmp/ITuning_ceph.conf', 'w') as f:
            f.write('[global]\n')
            f.write('public_network = {}\n'.format(public_network))
            f.write('cluster_network = {}\n'.format(cluster_network))
            f.write('osd objectstore = {}\n'.format(objectstore))
            f.write('[osd]\n')
            f.write('osd journal size = {}\n'.format(journal_size))
    
        conf = '/tmp/ITuning_ceph.conf'
        print "init" 
        for i in range(len(ips)):
            ceph_deploy.init(ips[i], password, hostnames[i])
        print "purge" 
        ceph_deploy.purge(name, hostnames)
        print "deploy" 
        ceph_deploy.deploy(name, mon_list, osdhost_list, disk_list, client_list, conf)
        print "create pool" 
        ceph_deploy.createrbdpool(len(disk_list), client_list[0])
        print "finish"

