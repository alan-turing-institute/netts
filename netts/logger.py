import logging
from pathlib import Path
from rich.logging import RichHandler

log_file = f"{Path(__file__).resolve().parent.parent}/netts_log.log"

logger = logging.getLogger('netts')

file_handler = logging.FileHandler(log_file)
console_handler = RichHandler(markup=True)

logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)

fmt_file = '%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
fmt_console = '%(message)s'

file_formatter = logging.Formatter(fmt_file)
console_formatter = logging.Formatter(fmt_console)

file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

stanza_logger = logging.getLogger("stanza")
stanza_logger.addHandler(file_handler)
stanza_logger.addHandler(console_handler)