import rpcapi
from oslo_log import log as logging
LOG = logging.getLogger(__name__)


class API(object):
    def __init__(self):
        self.rpcapi = rpcapi.JobAPI()

    def example_job(self, dict_args):
        LOG.info("from api: %s", dict_args)
        self.rpcapi.example_job(dict_args)

    def run_fio(self, dict_args):
        LOG.info("from api: %s", dict_args)
        self.rpcapi.run_fio(dict_args)
