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
                error_info = re.sub("u'", '', str(e))
                error_info = re.sub("'", '', str(e))
                jobinfo = {'status': "Failed: {}".format(error_info)}
                runfio.db.update_jobs(body['jobid'], **jobinfo)
            print e
        else:
            runfio.store_logfile_FS(log_dir)
            print "finish"

    def deploy(self, ctxt, body):
        LOG.info("deploy ceph: %s", body)

        deploy = ceph_deploy.Deploy()
        name = body["clustername"]

        osdhost_list = []
        client_list = []
        for key in body['nodenamekeys']:
            osdhost_list.append(body['nodename-{}'.format(key)])
        for key in body['clientnamekeys']:
            client_list.append(body['clientname-{}'.format(key)])

        nodepw_list = []
        clientpw_list = []
        for key in body['nodepwkeys']:
            nodepw_list.append(body['nodepw-{}'.format(key)])
        for key in body['clientpwkeys']:
            clientpw_list.append(body['clientpw-{}'.format(key)])

        nodeips = []
        clientips = []
        for key in body['nodeipkeys']:
            nodeips.append(body['nodeip-{}'.format(key)])
        for key in body['clientipkeys']:
            clientips.append(body['clientip-{}'.format(key)])

        ips = nodeips + clientips
        hostnames = osdhost_list + client_list
        password = nodepw_list + clientpw_list
    
        mon_list = []
        for mon in body['mon']:
            i = ips.index(mon)
            mon_list.append(osdhost_list[i]) 

        disk_list = []
        for key in body['nodekeys']:
            i = ips.index(body['node-{}'.format(key)])
            disk_list.append('{}:{}:{}'.format(
                osdhost_list[i],
                body['osddisk-{}'.format(key)],
                body['osdj-{}'.format(key)])
            )

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
            deploy.initenv(body['clusterid'], ips[i], password[i], hostnames[i])
        print "purge" 
        deploy.purge(body['clusterid'], name, hostnames)
        print "deploy" 
        deploy.deploy(body['clusterid'], name, mon_list, osdhost_list, disk_list, client_list, conf)
        print "create pool" 
        deploy.createrbdpool(len(disk_list), client_list[0])
        print "gen yaml file "
        deploy.gen_yaml_file(
            body['clusterid'],
            disk_list,
            osdhost_list,
            nodeips,
            nodepw_list,
            client_list,
            clientips,
            clientpw_list,
            public_network,
            cluster_network,
        )
        for client in client_list:
            print "install fio in {}".format(client)
            deploy.install_fio(client)
        for host in hostnames:
            print "reboot {}".format(host)
            deploy.reboot(host)
        for client in client_list:
            print "check and start fio server in {}".format(host)
            deploy.checkandstart_fioser(client)

        print "finish"

