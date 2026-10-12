import logging
from pathlib import Path
logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",datefmt="%H:%M:%S",force=True)

def validate_input(filepath):
    if not Path(filepath).is_file():
        logger.error("Input file not found: %s",filepath)
        return False
    logger.info("Input file validated: %s",filepath)
    return True
