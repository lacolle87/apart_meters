import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler('logs/app.log', maxBytes=100000, backupCount=5)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
