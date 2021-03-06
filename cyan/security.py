from http.client import CannotSendRequest
import os
import configparser

from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from . import common


def init_class(config_path: str=''):
    config_file = config_path or get_config_path()
    config = configparser.ConfigParser()

    config.read(config_file)

    site = config['SITE']['SiteUrl'] or r'http://localhost/'
    connection_string = config['SITE']['ConnectionString'] or r"Driver={SQL Server Native Client 11.0}; " \
                                                              "Server=.; Database=cosacs;uid=sa;pwd=;"
    driver_path = config['SITE']['DriverRelPath'] or r'\drivers\chromedriver.exe'
    use_remote = config['SELENIUM']['UseHub'] or False

    common.site_url = site
    common.driver_path = get_driver_path(driver_path)
    common.connection_string = connection_string

    if use_remote == 'True':
        hub_ip = config['SELENIUM']['HubIp'] or '192.168.30.8'
        hub_port = config['SELENIUM']['HubPort'] or '4444'
        hub_url = 'http://%s:%s/wd/hub' % (hub_ip, hub_port)

        print('using hub at: %s' % hub_url)

        desired_caps = {'platform': 'WINDOWS', 'browserName': 'chrome'}
        common.browser = webdriver.Remote(hub_url, desired_caps)
    else:
        common.browser = webdriver.Chrome(common.driver_path)

    common.browser.maximize_window()


def get_config_path():
    dir_path = get_project_path()

    return dir_path + r"\settings.ini"


def get_driver_path(driver_name: str):
    dir_path = get_project_path()

    return dir_path + driver_name


def get_project_path():
    path = os.path.abspath(__file__)

    return os.path.dirname(path).replace('\cyan\cyan', '')


def check_self(check_logging: bool=True):
    # global checking

    if common.checking:
        return
    else:
        common.checking = True
        if common.browser is None:
            init_class()

        if check_logging and is_logged() is False:
            login()


def login(user: str=None, password: str=None, config_path: str=''):
    """
    Log in into Cosacs application.

    :param user: User name
    :param password: Password

    Todo: Check if already logged | store u and pw
    """
    check_self(False)

    if is_logged():
        return
    else:
        config_file = config_path or get_config_path()
        config = configparser.ConfigParser()

        config.read(config_file)

        default_user = config['SITE']['User'] or r"user"
        default_pw = config['SITE']['Pw'] or r"password"

        u = user or default_user
        pw = password or default_pw

        common.browser.get(common.site_url)
        __wait_element_presence("#username")

        username_txt = common.browser.find_element(By.ID, r"username")
        __is_valid_element(username_txt)
        username_txt.send_keys(u)

        password_txt = common.browser.find_element(By.ID, r"password")
        __is_valid_element(password_txt)
        password_txt.send_keys(pw)

        xpath = "//button[contains(.,'Log In')]"
        login_btn = common.browser.find_element(By.XPATH, xpath)
        __is_valid_element(login_btn)
        login_btn.click()

        __wait_element_presence("logoff", By.ID, 40)
        __wait_element_presence("Warranty", By.LINK_TEXT, 10)


def logout():
    """
    Log off
    """
    check_self()

    logoff_btn = common.browser.find_element(By.ID, r"logoff")
    __is_valid_element(logoff_btn)
    logoff_btn.click()
    __wait_element_presence("#username")


def is_logged():
    try:
        if common.browser is None or __is_all_windows_closed():
            return False
        else:
            logoff_btn = common.browser.find_element(By.ID, r"logoff")
            return logoff_btn is not None
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False


def __is_valid_element(element: WebElement):
    assert (element is not None)
    assert element.is_displayed() is True, "element is not displayed on the page"
    assert element.is_enabled() is True, "element is not enabled"


def __is_all_windows_closed() -> bool:
    # global browser

    if common.browser is None:
        return True
    else:
        try:
            handles = common.browser.window_handles

            return handles is None or len(handles) < 1
        except CannotSendRequest:
            common.browser = None
            return True


def __wait_element_presence(search_filter, by: By=By.CSS_SELECTOR, timer: int=30):
    """
    Wait for an element to be loaded on the page.

    :param search_filter: The element identifier to search by
    :param timer: time to wait before it through a timeout error
    :param by: element filter type
    """
    WebDriverWait(common.browser, timeout=timer).until(
        ec.presence_of_element_located((by, search_filter))
    )


def __sys_admin_page():
    sysadmin_btn = common.browser.find_element(By.ID, r"profile")
    __is_valid_element(sysadmin_btn)
    sysadmin_btn.click()

