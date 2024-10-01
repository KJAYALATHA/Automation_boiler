import configparser
from custom_logger import configure_logger
import os

logger = configure_logger()

def load_config_file(file_path, section, key):
  
    value = None
    try:
        config = configparser.RawConfigParser()
        config.read(file_path)
        value = config.get(section, key)
    except IOError as e:
        logger.error("IO error while reading from properties file".format(e))
    return value

def ensure_directory_exists(directory_path):
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logger.info(f"{directory_path} is created")
    except Exception as e:
        logger.info(e)