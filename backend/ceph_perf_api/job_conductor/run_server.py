import time
import oslo_messaging
from oslo_config import cfg
import manager


def main():
    transport = oslo_messaging.get_transport(cfg.CONF)
    target = oslo_messaging.Target(topic='job', server='job-server')
    endpoints = [
        manager.Manager(),
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
