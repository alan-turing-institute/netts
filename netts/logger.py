import logging

log_file = "netts_log.log"
logger = logging.getLogger('netts')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file)
file_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

log_handler = logging.StreamHandler()
log_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.WARNING)
logger.addHandler(log_handler)

stanza_logger = logging.getLogger("stanza")
