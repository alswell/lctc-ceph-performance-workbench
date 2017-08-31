from oslo_config import cfg
import oslo_messaging as messaging


class JobAPI(object):
    def __init__(self):
        transport = messaging.get_transport(cfg.CONF)
        target = messaging.Target(topic='job', server='job-server')
        self.client = messaging.RPCClient(transport, target)

    def example_job(self, dict_args):
        print dict_args
        self.client.cast({}, 'example_job', body=dict_args)

    def run_fio(self, dict_args):
        print dict_args
        self.client.cast({}, 'run_fio', body=dict_args)

    def deploy(self, dict_args):
        print dict_args
        self.client.cast({}, 'deploy', body=dict_args)
