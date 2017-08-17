import rpcapi


class API(object):
    def __init__(self):
        self.rpcapi = rpcapi.JobAPI()

    def example_job(self, dict_args):
        self.rpcapi.example_job(dict_args)