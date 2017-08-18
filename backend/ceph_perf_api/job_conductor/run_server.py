import sys
import time
import oslo_messaging
from oslo_config import cfg
from common.log import setup_log


def main():
    setup_log()
    transport = oslo_messaging.get_transport(cfg.CONF)
    target = oslo_messaging.Target(topic='job', server='job-server')
    __import__('manager')
    endpoint = getattr(sys.modules['manager'], 'Manager')
    endpoints = [
        endpoint(),
    ]
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
