import logging
from colorlog import ColoredFormatter

formatter = ColoredFormatter(
    "%(log_color)s[%(levelname)s]%(reset)s %(message)s",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    }
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger('bugbounty')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def log_info(msg):
    logger.info(msg)

def log_warn(msg):
    logger.warning(msg)

def log_error(msg):
    logger.error(msg)

def log_critical(msg):
    logger.critical(msg)