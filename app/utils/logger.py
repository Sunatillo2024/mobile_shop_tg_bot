# logger.py
import logging
import sys

# Configure logging to output messages to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Create a logger instance to use in other files
the_logger = logging.getLogger(__name__)
