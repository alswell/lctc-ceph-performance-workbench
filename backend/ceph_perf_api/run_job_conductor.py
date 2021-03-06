#! /usr/bin/python
import os
import sys
import time
import oslo_messaging
from oslo_config import cfg

# file_path = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.join(file_path, ".."))
from common.log import setup_log


def load_endpoints():
    # __import__('manager')
    # endpoint = getattr(sys.modules['manager'], 'Manager')
    from job_conductor.manager import Manager
    endpoint = Manager
    endpoints = [
        endpoint(),
    ]
    return endpoints


def main():
    setup_log()
    transport = oslo_messaging.get_transport(cfg.CONF)
    target = oslo_messaging.Target(topic='job', server='job-server')
    endpoints = load_endpoints()
    server = oslo_messaging.get_rpc_server(transport, target, endpoints, executor='blocking')

    try:
        server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Stopping server ..."

    server.stop()
    server.wait()


if __name__ == '__main__':
    main()
