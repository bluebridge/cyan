__author__ = 'ashaD'
import string
from selenium.webdriver.common.by import By

from cyan import nav, input, dom, security, common

# Generic function to add or deny permission to different screens in cosacs


def add_deny_permission(permission_screen_name: string, permission_type: string, menu: string, menu_item: string):
    input.click_element("profile", By.ID)
    dom.wait_presence_of_element("roleLink", 10, By.CLASS_NAME)
    input.click_element("roleLink", By.CLASS_NAME)
    dom.wait_presence_of_element("page-heading", 50, By.ID)
    dom.wait(3)
    xpath_row = "//tr[td[text()= '%s']]" % permission_screen_name
    permission_row = dom.get_element(xpath_row, By.XPATH)
    xpath_for_permission_type = xpath_row + "//input[@type='checkbox' and @name='%s']" % permission_type
    element = dom.get_element(xpath_for_permission_type, By.XPATH)
    dom.scroll_element_to_view_1(permission_screen_name)
    if not element.is_selected():
        element.click()
    security.logout()
    security.login(common.username, common.password)
    dom.wait_presence_of_element("home", 10, By.ID)
    if permission_type == "Allow":

        nav.menu(menu, menu_item)
        dom.wait_for_text_present(menu_item, "#body > div > h1", 30, By.CSS_SELECTOR)
    else:
        menu_options=nav.get_menu_options(menu)
        for x in menu_options:
            if x == menu_item:
                assert "Menu Item still exists even after denying permission"


def go_to_system_settings_page():
    nav.menu("Configuration", "System Settings")


def verify_system_settings(menu_name: string, system_setting_name: string, system_setting_description: string):
        go_to_system_settings_page()
        xpath ="//li[contains(@class,'ng-scope')]//a[@class='menu_element ng-binding' and text()='%s']" % menu_name
        dom.wait_presence_of_element(xpath, 10, by=By.XPATH)
        input.click_element(xpath, by=By.XPATH)
        dom.wait(2)
        xpath = "//h4[@class='text-center ng-binding' and text()='%s']" % menu_name
        dom.wait_presence_of_element(xpath, 10, by=By.XPATH)

        xpath_system_setting_name = "//tr[contains(@class,'ng-scope')]//td[@class='ng-binding' and text()='%s']"\
                                    % system_setting_name
        xpath_system_setting_description = "//tr[contains(@class,'ng-scope')]//td[@class='ng-binding' and text()='%s']"\
                                           % system_setting_description
        system_setting = [xpath_system_setting_name, xpath_system_setting_description]
        for x in system_setting:
            system_setting_name = dom.get_element(x, by=By.XPATH)
            system_setting_name.is_displayed()


def verify_audit_details(audit_category: string, audit_type: string):
    xpath_type = "//td[@class= 'type']/a[text()='%s'][1]" % (audit_type)
    xpath_category = "//td[@class='category']/a[text()='%s'][1]" % (audit_category)
    xpath_values = [xpath_type, xpath_category]
    for x in xpath_values:
        element = dom.get_element(x, By.XPATH)
        element.is_displayed()

