import logging

LOG_LEVELS = {
    logging.NOTSET: 'sample',
    logging.DEBUG: 'debug',
    logging.INFO: 'info',
    logging.WARNING: 'warning',
    logging.ERROR: 'error',
    logging.FATAL: 'fatal',
}
DEFAULT_LOG_LEVEL = 'error'

LOG_LEVELS_MAP = {v: k for k, v in LOG_LEVELS.items()}
