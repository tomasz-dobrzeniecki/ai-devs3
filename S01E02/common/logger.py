from loguru import logger
import sys

def setup_logger(logfile=None, level="INFO"):
    logger.remove()
    logger.add(sys.stderr, level=level)  # Console with colors
    if logfile:
        logger.add(logfile, level=level, rotation="1 MB")
    return logger