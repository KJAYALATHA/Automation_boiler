import os
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from file_operations import load_config_file
from custom_logger import configure_logger


config_path = os.path.join(os.getcwd(), "config.cfg")
browser_wait = load_config_file(config_path, str('Input'), "BROWSER_WAIT")
element_wait = load_config_file(config_path, str('Input'), "ELEMENT_WAIT")

class SeleniumHelperPage():

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10
        self.wait = WebDriverWait(self.driver, 30)
        self.log = configure_logger()

    def find_element(self, locator):
        try:
            return self.driver.find_element(*locator)
        except Exception as e:
            self.log.error("Exception {0} while finding element".format(e))
            return None

    def click(self, *locator):
        result = False
        try:
            element = self.element_visible(locator)
            element.click()
            result = True
            self.log.info(
                "Web element {0} : {1} successfully clicked".format(
                    locator[0], locator[1]))
        except NoSuchElementException as ex:
            self.log.error("Failed to click Web element {0} : {1},"
                           " displayed with error {2}".format(locator[0],
                                                              locator[1],
                                                              ex.msg))
        except Exception as e:
            self.log.error("Exception {}".format(e))
        return result
    
    
    def wait_for_element(self, locator):
        try:
            wait = WebDriverWait(self.driver, int(browser_wait) * 2)
            element = wait.until(ec.visibility_of_element_located(locator))
            return element
        except NoSuchElementException as e:
            self.log.info("Exception - No such element {0}".format(e))
            return None

    def is_element_visible(self, locator):
        try:
            WebDriverWait(self.driver, int(element_wait), poll_frequency=1,
                          ignored_exceptions=[NoSuchElementException]).until(
                ec.visibility_of_element_located(locator))
            return True
        except Exception as e:
            self.log.info("Exception - No such element {0}".format(e))
            return False

    def element_visible(self, locator):
        try:
            element = WebDriverWait(self.driver, int(browser_wait)).until(
                ec.visibility_of_element_located(locator))
            # self.driver.execute_script("arguments[0].scrollIntoView();",
            #                            element)
            self.log.info("Web element {0} : {1} "
                          "was visible".format(locator[0], locator[1]))
            return element
        except StaleElementReferenceException as ser:
            self.log.error("Stale element exception {0} was displayed during"
                           " element {1} : {2} location ".format(ser.msg,
                                                                 locator[0],
                                                                 locator[1]))
        except NoSuchElementException as ex:
            self.log.error("No such element exception {0} was displayed during"
                           "element {1} : {2} location".format(ex.msg,
                                                               locator[0],
                                                               locator[1]))
        except TimeoutException as et:
            self.log.error("Script timed out with message {0} during "
                           "element {1} : {2} location".format(et.msg,
                                                               locator[0],
                                                               locator[1]))
            
    def clear_text(self, *locator):
        """
        wrapper function to clear text in the type text web element
        :param locator:
        :return: True is text is entered successfully else False
        """
        try:
            element = self.find_element(locator)
            element.clear()
            self.log.info("Cleared text field Web element {} : {}".
                          format(locator[0], locator[1]))
            return True
        except NoSuchElementException as ex:
            self.log.error("Failed to clear value for text web element {} : {},displayed with error message {}".
                           format(locator[0], locator[1], ex.msg))
            return False

    def set_text(self, data, *locator):
        try:
            element = self.find_element(locator)
            element.send_keys(str(data))
            time.sleep(1)
            self.log.info("Web element {} : {} was located and entered with value : {}".
                          format(locator[0], locator[1], str(data)))
            return True
        except NoSuchElementException as ex:
            self.log.error("Failed to enter value {} for web element {} : {},displayed with error message {}".
                           format(str(data), locator[0], locator[1], ex.msg))
            return False

    def js_wait_for_condition(self, js_script, timeout):
        result = False
        try:
            for x in range(1, timeout):
                x = self.driver.execute_script("return " + js_script)
                if x:
                    result = True
                time.sleep(1)
        except Exception as e:
            self.log.error("Exception {} occurred while waiting for JS condition".format(e))
            result = False
        return result

    def wait_for_page_load(self, driver):
        try:
            WebDriverWait(driver, 120).until(lambda wde: wde.execute_script('return document.readyState') == 'complete')
        except JavascriptException as je:
            self.log.error('error, waiting for page load, {}'.format(self.wait_for_page_load.__name__), je)
            return False
