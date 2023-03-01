import logging
import datetime

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a custom log formatter with a timestamp
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Create a file handler to write the log data to a file
file_handler = logging.FileHandler('all_data.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Log some data with timestamps

def write_in_log(str):
    logger.info(str)


