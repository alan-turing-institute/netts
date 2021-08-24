import logging
import os

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logger = logging.getLogger("netspy")

if logger.level == 0:
    logger.setLevel(LOGLEVEL)

log_handler = logging.StreamHandler()
log_formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
log_handler.setFormatter(log_formatter)
if not logger.hasHandlers():
    logger.addHandler(log_handler)

stanza_logger = logging.getLogger("stanza")
stanza_logger.setLevel(logging.ERROR)
