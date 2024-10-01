import logging
import os



def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_path = os.path.join(os.getcwd(), 'Logs')
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_name = os.path.join(file_path, "ESIC_RPA_Log.log")
    handler = logging.FileHandler(f"{file_name}",mode='w')
    logger.info(f"log file createddd {file_name}")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger