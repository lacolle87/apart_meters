import logging
import os


def setup_logger():
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_file = os.path.join(logs_dir, 'app.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
