import logging
from oslo_log import log


def setup_log():
    root_log = log.getLogger().logger
    handler = logging.FileHandler("/log.log")
    formatter = logging.Formatter("[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s")
    handler.setFormatter(formatter)
    root_log.addHandler(handler)
    root_log.setLevel(logging.DEBUG)
