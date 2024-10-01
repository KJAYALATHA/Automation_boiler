from file_operations import load_config_file
import os
from browser_operations import get_browser



config_path = os.path.join(os.getcwd(), "config.cfg")
def get_login_page():
    portal_url =load_config_file(config_path, str('Portal_details'), "portal_url")
    driver = get_browser(portal_url)
    return driver