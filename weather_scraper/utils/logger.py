import logging
import os

def get_logger() -> logging.Logger:
    logger = logging.getLogger()
    try:
        logger.setLevel(os.environ['LOG_LEVEL'])
    except KeyError:
        logger.setLevel('INFO')

    return logger