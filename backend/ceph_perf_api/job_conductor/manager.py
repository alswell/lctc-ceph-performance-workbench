import time
import os
import sys
import re
import json


file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_path, ".."))
from fiotest.fio_test import run_suite
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

            runfio.store_logfile_FS(log_dir)
        except Exception, e:
            jobinfo = {'status': "Failed"}
            runfio.db.update_jobs(body['jobid'], **jobinfo)
            print e
        else:
            print "finish"
