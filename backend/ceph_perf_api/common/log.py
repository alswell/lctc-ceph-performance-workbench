import logging
from oslo_log import log

logging.addHandler()
def setup_log():
    root_log = log.getLogger().logger
    handler = logging.FileHandler("/log.log")
    formatter = logging.Formatter("[%(levelname)s][%(asctime)s](%(process)d|%(thread)d)"
                                  "%(pathname)s @%(funcName)s:%(lineno)d # %(message)s")
    handler.setFormatter(formatter)
    root_log.addHandler(handler)
    root_log.setLevel(logging.DEBUG)
