import logging


def setup_logger(model_name, log_file):
    # Configure the logging format
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logger = logging.getLogger(model_name)
    # logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)
    # file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
