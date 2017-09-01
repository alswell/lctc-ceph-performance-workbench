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
                jobinfo = {'status': "Failed"}
                runfio.db.update_jobs(body['jobid'], **jobinfo)
            print e
        else:
            runfio.store_logfile_FS(log_dir)
            print "finish"

    def deploy(self, ctxt, body):
        LOG.info("deploy ceph: %s", body)

        ips = ['192.168.230.218', '192.168.230.201', '192.168.230.196', '192.168.230.199']
        password = 'passw0rd'
        name = "mycluster1"
        osdhost_list = ['ceph-3', 'ceph-1', 'ceph-2']
        client_list = ['client-1']
    
        mon_list = [osdhost_list[1]]
        disk_list = [osdhost_list[1]+':/dev/sda:/dev/sdc', osdhost_list[2]+':/dev/sda:/dev/sdc', osdhost_list[0]+':sda:/dev/sdb']
    
        hostnames = osdhost_list + client_list
    
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
    
        #for i in range(len(ips)):
        #    init(ips[i], password, hostnames[i])
    
        ceph_deploy.purge(name, hostnames)
        ceph_deploy.deploy(name, mon_list, osdhost_list, disk_list, client_list, conf)
        ceph_deploy.createrbdpool(len(disk_list), client_list[0])

