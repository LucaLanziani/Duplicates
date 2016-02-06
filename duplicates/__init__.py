import logging


def start_logger(level='INFO'):
    logging.basicConfig()
    log = logging.getLogger(__name__)
    log.setLevel(level)
    log.info('STARTING')
    log.debug('Log level set to %s', logging.getLevelName(log.getEffectiveLevel()))
