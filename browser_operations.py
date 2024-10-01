from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException
from custom_logger import configure_logger

logger = configure_logger()
def get_chrome_driver():  
  
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)
        logger.info('initiated chrome driver with web driver-manager automatically')
        return driver
    except (SessionNotCreatedException, ValueError, TypeError, AttributeError):
        chrome_driver_path = Service(os.path.join(os.getcwd(), "Driver", "chromedriver.exe"))
        driver = webdriver.Chrome(service=chrome_driver_path, options=chrome_options)
        logger.info("driver intiated by chromeDriver that we given in Driver folder")
        return driver
    except Exception as e:
        if "ERR_NAME_NOT_RESOLVED" in str(e):
            logger.info("Error: INTERNET FAILDE.")
        else:
            logger.info("An error occurred in driver initialization: {e}")
        return None
def get_browser(url):
    try:
        web_driver = get_chrome_driver()
        if web_driver is not None:
            web_driver.get(url)
            web_driver.maximize_window()
        else:
            logger.error("Failed to initialize the chrome web driver")
            exit(-1)
        return web_driver
    except Exception as ex:
        logger.error("Function get_browser failed with error :{}".format(ex))
    
