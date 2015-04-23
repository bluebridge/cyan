import string
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from cyan import input, security, common, dom


class MenuItem(object):
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.nodes = []

def go_home():
    """
    Navigate to the Home page
    """
    security.check_self()
    input.click_element(r"home", By.ID)


def refresh():
    """
    Refresh current page
    """
    security.check_self()
    common.browser.refresh()


def go(url: string):
    """
    Navigate to a specific Url.
    :param url: The url to go to. It can a relative or absolute url.
    """
    security.check_self()
    if not url.startswith(common.site_url):
        url = r"".join([common.site_url, url])

    common.browser.get(url)


def multi_menu(menu_hierarchy: string, delimiter: string=","):
    """
    Click on a navigation menu item (work on multi levels menu)
    :param menu_hierarchy: The menu item hierarchy as string separated by delimiter
    :param delimiter: The delimiter that separate the menu items
    """
    security.check_self()
    items = menu_hierarchy.split(delimiter)

    for item in items:
        input.click_element(item, By.LINK_TEXT)


def menu(parent_item: string, child_item: string):
    """
    Click on a navigation menu item (only work on a 2 level menu)
    :param parent_item: The parent menu item
    :param child_item: The sub menu item
    """
    security.check_self()
    input.click_element(parent_item, by=By.LINK_TEXT)
    dom.wait(0.5)
    input.click_element(child_item, by=By.LINK_TEXT)


def cascade_menu(parent_item, nameHover_item, child_item):
    """

    :param parent_item: The Parent Menu Item (Link Text)
    :param CSSHover_item:  The Hover Menu Item (Text that is displayed)
    :param child_item:  The child menu item that is wanted (Link Text)
    :return:
    """
    # confirm that nothing is selected
    body = dom.get_element(".body", By.CSS_SELECTOR)
    body.click()

    # get the items that contain more options within the dropdowns
    CSSHover_item = ' .navbar-nav .dropdown-submenu'
    finalResult = '.dropdown-submenu .dropdown-menu li'
    parentCSS = '.nav-collapse.navbar-inverse-collapse .nav.navbar-nav li.dropdown a.dropdown-toggle'

    # Get the initial menu item
    parentMenu = dom.get_elements(parentCSS, By.CSS_SELECTOR)
    elementParent = parentMenu[0]
    for x in range(0, len(parentMenu)):
        word = parentMenu[x].text
        if word.upper() == parent_item.upper():
            elementParent = parentMenu[x]
            break

    # Get the hover items
    hover_item = dom.get_elements(CSSHover_item, By.CSS_SELECTOR)
    subMenu = hover_item[0]
    for x in range(0, len(hover_item)):
        word = hover_item[x]
        wordResult = word.get_attribute("textContent")
        if nameHover_item in wordResult:
            if child_item in wordResult:
                subMenu = hover_item[x]
                break

    # get the final click
    allFinalItems = dom.get_elements(finalResult, By.CSS_SELECTOR)
    elementChild = allFinalItems[0]
    expectedResult = child_item.replace(" ", "")

    # Get the final menu item
    for x in range(0, len(allFinalItems)):
        textResult = allFinalItems[x].get_attribute("textContent")
        textResults1 = textResult.replace(" ", "")
        textResults2 = textResults1.replace("\n", "")

        if textResults2.upper() == expectedResult.upper():
            elementChild = allFinalItems[x]
            break

    # preform the result
    hover = ActionChains(common.browser)
    hover.click(elementParent)
    hover.move_to_element(subMenu)
    hover.click(elementChild)
    hover.perform()


def menu_CSS(parent_item: string, child_item: string):
    """

    :param parent_item: The Parent Menu Item (Link Text)
    :param child_item:  The child menu item that is wanted (Link Text)
    :return:
    """
    # confirm that nothing is selected
    body = dom.get_element(".body", By.CSS_SELECTOR)
    body.click()

    # get the css for the menus
    parentCSS = '.nav.navbar-nav li.dropdown a.dropdown-toggle'
    childCSS = '.navbar-nav li.dropdown ul.dropdown-menu>li:not(.dropdown-submenu) a'

    # get the child
    allFinalItems = dom.get_elements(childCSS, By.CSS_SELECTOR)
    elementChild = allFinalItems[0]
    expectedResult = child_item.replace(" ", "")

    for x in range(0, len(allFinalItems)):
        textResult = allFinalItems[x].get_attribute("textContent")
        textResults = textResult.replace(" ", "")
        textResults = textResults.replace("\n", "")

        if textResults.upper() == expectedResult.upper():
            elementChild = allFinalItems[x]
            break

    # Get the 1st Item from the text
    parentMenu = dom.get_elements(parentCSS, By.CSS_SELECTOR)
    elementParent = parentMenu[0]
    for x in range(0, len(parentMenu)):
        word = parentMenu[x].text
        if word == parent_item:
            elementParent = parentMenu[x]
            break

    # Hover on to the 2nd menu item
    hover = ActionChains(common.browser)
    hover.click(elementParent)
    hover.click(elementChild)
    hover.perform()


#
# Uses the parent menu name to return a list of all the sub menu's that are available
#
def get_menu_options(parent_item: string):
    menuItems = list()
    input.click_element(parent_item, by=By.LINK_TEXT)
    children = dom.get_elements(".dropdown.open li", By.CSS_SELECTOR)
    length = len(children)
    for x in range(0, length):
        item = children[x].text
        if item:
            menuItems.append(item)
    return menuItems


#
# Uses the parent menu name to return a list of all the sub menu's that are available including sub menu's
#
def get_all_menu_options(parent_item: string):
    menuItems = list()
    input.click_element(parent_item, by=By.LINK_TEXT)
    children = dom.get_elements('a[href^="/Merchandising"]', By.CSS_SELECTOR)

    length = len(children)
    for x in range(0, length):
        item = children[x].get_attribute('innerHTML')
        if item:
            menuItems.append(item)
        else:
            aaa = 0  # Is there a sub menu
    return menuItems


def quit_browser():
    # global browser
    # global checking

    if common.browser:
        common.browser.quit()

    common.checking = False
    common.browser = None


def get_main_menu() -> list:
    menu_list = []
    parent_menu = dom.get_elements("#mainMenu > li", By.CSS_SELECTOR)

    if not parent_menu:
        return menu_list

    for sub_menu in parent_menu:
        menu_item = get_menu_item(sub_menu)
        menu_list.append(menu_item)

    return menu_list


def get_menu_item(ele: WebElement) -> MenuItem:
    """

    :param ele:
    :return:
    """
    url = ele.find_element_by_tag_name('a')

    menu_title = url.text
    menu_url = url.get_attribute('href')
    menu_item = MenuItem(menu_title, menu_url)
    nodes = ele.find_elements_by_css_selector("ul > li")

    for node in nodes:
        sub_menu = get_menu_item(node)
        menu_item.nodes.append(sub_menu)

    return menu_item


def get_web_request_status_code(url: string):

    try:
        r = requests.head(url)
        return r.status_code
    except requests.ConnectionError:
        # failed to connect
        return -1