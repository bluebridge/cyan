"""
    ---------------------------------------------------------------------

    This module contains the functionality that related to DOM tree like:
        * Finding DOM's elements.
        * Checking the elements state (Present, visible,..etc.)

    ---------------------------------------------------------------------

"""

from http.client import CannotSendRequest
import datetime
import time
import string
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.remote.webelement import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import sys

sys.path.append("../..")
from . import security, common


def get_browser() -> webdriver.chrome.webdriver.WebDriver:
    """
    Get the shared web driver.

    :return: The web driver
    :rtype: WebDriver
    """
    return common.browser


def wait_for_text_present(text_to_present: str, text_element: str, by: By=By.CSS_SELECTOR, timer: int=10):
    """
    Wait for a string literal to be present on the page.

    :param text_to_present: The string to wait for its present
    :param text_element: The dom element whose has the string as its value.
    :param timer: Time to wait before it's timeout
    :param by: The string's attribute
    """
    security.check_self()

    wait_visibility_of_element(text_element, by, timer)

    WebDriverWait(common.browser, timeout=10).until(
        element_text_available_callback(text_to_present, text_element, by))


def wait_presence_of_element(search_filter, by: By=By.CSS_SELECTOR, timer: int=10):
    """
    Wait for an element to be loaded on the page

    :param search_filter: The element identifier to search by
    :param timer: time to wait before it through a timeout error
    :param by: element filter type
    """
    security.check_self()

    WebDriverWait(common.browser, timeout=timer).until(
        ec.presence_of_element_located((by, search_filter))
    )


def wait_presence_of_element_by_text(element_text: str, timer: int=10,
                                     search_type: common.TextSearchType=common.TextSearchType.Contain):
    """
    Wait for an element to be loaded on the page

    :param element_text: The element text to search by
    :param timer: time to wait before it through a timeout error
    """
    security.check_self()

    xpath = common.get_attr_xpath("//.", "text()", element_text, search_type)

    WebDriverWait(common.browser, timeout=timer).until(
        ec.presence_of_element_located((By.XPATH, xpath))
    )


def element_text_available_callback(element_text: str, element: str, by: By=By.CSS_SELECTOR):
    """

    :param element_text:
    :param element:
    :param by:
    :return:
    """
    security.check_self()

    el = get_element(element, by)

    def callback(_browser):
        _browser.find_element(by, element)

        if (el is not None) and (el.text == element_text):
            return True
        else:
            return False

    return callback


def wait_visibility_of_element(search_filter, element_by: By=By.CSS_SELECTOR, timer: int=10,
                               msg: str='Waiting for element timed out'):
    """
    Wait for an element to be loaded and become visible on the page.

    :param search_filter: The element identifier to search by
    :param timer: time to wait before it through a timeout error
    :param element_by: element filter type
    """
    security.check_self()
    WebDriverWait(common.browser, timer) \
        .until(lambda s: s.find_element(element_by, search_filter).is_displayed(), msg)


def wait_for_element_enabled(search_filter, element_by: By=By.CSS_SELECTOR, timer: int=10,
                               msg: str='Waiting for element timed out'):
    """
    Wait for an element to be enabled on the page.

    :param search_filter: The element identifier to search by
    :param timer: time to wait before it through a timeout error
    :param element_by: element filter type
    """
    security.check_self()
    WebDriverWait(common.browser, timer) \
        .until(lambda s: s.find_element(element_by, search_filter).is_enabled(), msg)


def wait_non_visibility_of_element(search_filter, element_by: By=By.CSS_SELECTOR, timer: int=10,
                               msg: str='Waiting for element timed out'):
    """
    Wait for an element to be loaded and become visible on the page.

    :param search_filter: The element identifier to search by
    :param timer: time to wait before it through a timeout error
    :param element_by: element filter type
    """
    security.check_self()
    WebDriverWait(common.browser, timer) \
        .until_not(lambda s: s.find_element(element_by, search_filter).is_displayed(), msg)


def wait_visibility_of_element_by_text(element_text: str, timer: int=10,
                                       msg: str='Waiting for element timed out',
                                       search_type: common.TextSearchType=common.TextSearchType.Contain):
    """
    Wait for an element to be loaded and become visible on the page.

    :param element_text: The element's text to search by
    :param timer: time to wait before it through a timeout error
    :param msg: Message to fire when timeout error thrown
    """
    security.check_self()
    xpath = common.get_attr_xpath("//.", "text()", element_text, search_type)

    WebDriverWait(common.browser, timer) \
        .until(lambda s: s.find_element(By.XPATH, xpath).is_displayed(), msg)


def wait_visibility_of_ng_element(model_name: str, timer: int=10, element_tag: str='*', angular_prefix: str='ng',
                                  msg: str='Waiting for element timed out'):
    """
    Wait for an element to be loaded and become visible on the page.

    :param model_name: Angular model binding name
    :param element_tag: The element's html tag
    :param angular_prefix: angular html data prefix
    :param element_tag: DOM element's tag
    :param timer: time to wait before it through a timeout error
    :param msg: Message to fire when timeout error thrown
    """
    security.check_self()

    attr_name = "%s-model" % angular_prefix
    xpath = "//%s[@%s='%s']" % (element_tag, attr_name, model_name)

    WebDriverWait(common.browser, timer) \
        .until(lambda s: s.find_element(By.XPATH, xpath).is_displayed(), msg)


def is_element_present(search_filter: str, element_by: By=By.CSS_SELECTOR) -> bool:
    """
    Check the present of an element on the current page.

    :param search_filter: the element filter value:
    :param element_by: the element filter type
    """
    security.check_self()

    try:
        return get_element(search_filter, element_by) is not None
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False
        # assert 0, "can't find element: '%s' using its '%s'" % (search_filter, element_by)


def is_element_visible(search_filter: str, element_by: By=By.CSS_SELECTOR) -> bool:
    security.check_self()

    try:
        element = get_element(search_filter, element_by)
        return element.is_displayed()
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False


def is_web_element_visible(element) -> bool:
    security.check_self()

    try:
        return element.is_displayed()
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False


def is_element_visible_text(element_text: str) -> bool:
    state = False

    try:
        ele = get_element_by_text(element_text)
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False

    if ele:
        state = ele.is_displayed()

    return state


def is_element_visible_attr(attr_name: str, attr_value: str, tag: str='input') -> bool:
    state = False
    xpath = "//{0}[@{1}='{2}']".format(tag, attr_name, attr_value)
    ele = common.browser.find_elements_by_xpath(xpath)

    if ele:
        state = ele.is_displayed()

    return state


def is_element_disabled(css: str)-> bool:
    """
    Checks if the element has the 'disabled' class attached to the element.

    :param css:
    :return:
    """
    css += ' .disabled'

    try:

        return get_element(css) is not None
    except:
        return False

    return False


def is_element_selected(search_filter: str, element_by: By=By.CSS_SELECTOR) -> bool:
    """
    To check if a tick box is selected.

    :param search_filter:
    :param element_by:
    :return:
    """
    security.check_self()

    try:
        element = get_element(search_filter, element_by)
        return element.is_selected()
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False


def is_web_element_selected(element: WebElement) -> bool:
    """
    To check if a tick box is selected.

    :param element:
    :return:
    """
    security.check_self()

    try:
        return element.is_selected()
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False


def is_element_enabled(search_filter: str, element_by: By=By.CSS_SELECTOR) -> bool:
    security.check_self()

    try:
        element = get_element(search_filter, element_by)
        return element.is_enabled()
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False


def select_from_dropdown(xpath: str, selection: str):
    dropdown = get_element(xpath, By.XPATH)
    dropdown.click()
    wait(0.5)

    css = "div.list-item:nth-child(" + selection + ")"  # Select the nth option from the drop down list
    option = get_element(css)
    option.click()
    wait(0.5)


def select_from_dropdown_search(css: str, selection: str):
    css1 = css + ' .play'
    we = get_elements(css1)
    we[0].click()  # Open up the entry box

    css2 = css + ' input'
    wait(1)
    we = get_element(css2)
    we.send_keys(Keys.CONTROL + "a")
    we.send_keys(selection)

    # Now click on the search result
    css3 = css + ' .list-options .list-item'
    wait_presence_of_element(css3)
    we = get_elements(css3)
    we[0].click()


def get_Options_from_dropdown_search(css: str):
    options = []

    css1 = css + ' .play'
    wait_presence_of_element(css)
    we = get_element(css1)
    we.click()  # Open up the entry box

    new_css = '.list-options .list-item'
    we = get_elements(new_css)
    count = len(we)

    for x in range(0, (count - 1)):
        name = we[x].text
        options.append(name)

    css2 = css + ' input'
    we = get_element(css2)
    we.send_keys(webdriver.common.keys.Keys.ESCAPE)

    return options


def select_from_dropdown_CSS(css: str, selection: str):
    dropdown = get_element(css)
    dropdown.click()
    wait(0.5)

    css = "div.list-item:nth-child(" + selection + ")"  # Select the nth option from the drop down list
    option = get_element(css)
    option.click()
    wait(0.5)


def select_from_add(css: str, name: str):
    """
    Enter the 'name' in the search text box then click on 'Enter' to select

    :param css:
    :param name:
    """
    we = get_element(css)
    input = we.find_element(By.CSS_SELECTOR, 'input')
    input.send_keys(name)
    input.send_keys(Keys.ENTER)

    # Now click on the 'Add'
    we = get_element(css)
    add = we.find_element(By.CSS_SELECTOR, 'button')
    add.click()


def select_from_dropdown_no_search(css: str, selection: str):
    dropdown = get_element(css)

    for option in dropdown.find_elements_by_tag_name('option'):
        if option.text == selection:
            option.click()
            break

    wait(0.5)


def validate_element(element: WebElement):
    security.check_self()

    assert (element is not None)
    assert (element.is_displayed()), "element is not displayed on the page"
    assert (element.is_enabled()), "element is not enabled"


def get_element(search_filter: str, by: By=By.CSS_SELECTOR) -> WebElement:
    """
    Get an element by its identifier.

    :param search_filter: The element identifier to search by
    :param by: Element's filter type
    :return:
    :rtype: WebElement
    """
    security.check_self()
    return common.browser.find_element(by, search_filter)


def get_element_by_value(value: str, search_type: common.TextSearchType=common.TextSearchType.Contain) -> WebElement:
    """
    Get DOM element by its value.

    :param value: Element's value
    :return: The element
    """

    security.check_self()

    xpath = common.get_attr_xpath("//*", "value()", value, search_type)

    return common.browser.find_elements_by_xpath(xpath)


def get_element_by_text(value: str, tag: str='*',
                        search_type: common.TextSearchType=common.TextSearchType.Contain) -> WebElement:
    """
    Get DOM element by its text.

    :param value:
    :param search_type:
    :return:
    """

    security.check_self()

    prefix = "//%s" % tag

    xpath = common.get_attr_xpath(prefix, 'normalize-space(text())', value, search_type)
    ele = get_element(xpath, By.XPATH)

    if ele:
        return ele
    else:
        return None


def get_element_by_attribute(attribute_name: str, attribute_value: str, element_tag: str='*',
                             search_type: common.TextSearchType=common.TextSearchType.Exact) -> WebElement:
    """
    Get DOM element by its attribute.

    :param attribute_name: Attribute name
    :param attribute_value: Attribute value
    :param element_tag: DOM element's tag
    :return: The element
    """

    security.check_self()

    prefix = "//%s" % element_tag

    xpath = common.get_attr_xpath(prefix, attribute_name, attribute_value, search_type)

    return common.browser.find_element_by_xpath(xpath)


def get_element_by_angular_model(model_name: str, element_tag: str='*', angular_prefix: str='ng') -> WebElement:
    """
    Get DOM element by its AngularJs model's binding.

    :param model_name: Angular model binding name
    :param element_tag: The element's html tag
    :param angular_prefix: angular html data prefix
    :param element_tag: DOM element's tag
    :return: The element
    """

    attr_name = "%s-model" % angular_prefix
    return get_element_by_attribute(attr_name, model_name, element_tag)


def get_elements(search_filter: str, by: By=By.CSS_SELECTOR):
    """
    Get all element by its identifier.

    :param search_filter: The elements identifier to search by
    :param by: element filter type
    :return:
    """
    security.check_self()

    return common.browser.find_elements(by, search_filter)


def get_label_by_partial_text(label_text: str) -> WebElement:
    """
    Get a label by its partial text.

    :param label_text: label's partial text
    :return: The found label as WebElement
    """

    return get_label_by_text(label_text, common.TextSearchType.Contain)


def get_label_by_text(label_text: str, search_type: common.TextSearchType=common.TextSearchType.Exact) -> WebElement:
    """
    Get a label by its text.

    :param label_text: label's text
    :return: The found label as WebElement
    """

    security.check_self()

    xpath = common.get_attr_xpath("//label", "text()", label_text, search_type)
    return get_element(xpath, By.XPATH)


def get_link_by_text(link_text: str) -> WebElement:
    """
    Get a link by its text.

    :param label_text: label's text
    :return: The found label as WebElement
    """
    security.check_self()
    link = common.browser.find_element_by_link_text(link_text)

    return link


def all_windows_closed() -> bool:
    security.check_self()
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


def wait(timer: int):
    time.sleep(timer)


def scroll_to_bottom():
    """
    takes a screenshot of the current web page and saves it in a folder called Screenshots.

    """
    security.check_self()
    reached_bottom = False
    while not reached_bottom:
        reached_bottom = common.browser.execute_script(
            "return $(document).height() == ($(window).height() + $(window).scrollTop());")
        common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait(2)


def scroll_to_top():
    """
    Scrolls the page to the top.

    """
    security.check_self()
    reached_top = False
    while not reached_top:
        reached_top = common.browser.execute_script(
            "return $(document).height() == ($(window).height() + $(window).scrollTop());")
        common.browser.execute_script("window.scrollTo(0, 0);")
        wait(2)

def scroll_down():
    """
    scroll to the bottom of the page
    """
    security.check_self()
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_down_by(distance: int):
    security.check_self()
    common.browser.execute_script("window.scrollBy(0, {value})".format(value=distance))


def scroll_up(distance):
    security.check_self()
    text = "window.scrollBy(0,-" + distance + ")"
    common.browser.execute_script(text, "")


def scroll_element_into_view(elementWe):
    y = elementWe.location['y'] - 50
    common.browser.execute_script('window.scrollTo(0, {0})'.format(y))
    wait(0.5)


def execute_script(script, ele):
    common.browser.execute_script(script, ele)


def screen_shot(file_name: str, file_directory: str='./Screenshots'):
    """
    takes a screen-shot of the current web page and saves. If the specified folder don't exists, it will be created

    :param file_name: name of the file to be saved. The current time in the format YYYYMMDD_HHMMSS will be added as suffix to the file name
    :param file_directory: destination folder
    """

    file_directory = file_directory or './Screenshots'
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)

    file_name = '%s-%s.png' % (datetime.datetime.now().strftime('%Y%m%d_%H%M%S'), file_name)

    common.browser.get_screenshot_as_file('%s/%s' % (file_directory, file_name))


def click_Calendar(dateToChangeTo):
    """
    change the day/month/year on the calendar pop up as expected format for dateToChangeTo is Mon 21 May, 2014

    :rtype : object
    """

    # variables
    # Year
    calendarYearSelected = '.ui-datepicker-year [selected="selected"]'
    calendarYearToSelect = '.ui-datepicker-year [value="'  # requires year to select and "]
    calendarYearOptions = '.ui-datepicker-year'
    # month
    calendarMonthSelected = '.ui-datepicker-month [selected="selected"]'
    calendarMonthOptions = '[class="ui-datepicker-month"]'
    calendarMonthToSelect = '[class="ui-datepicker-month"] [value="'  # requires month to select and "]
    # day
    calendarAllDates = '.ui-state-default'


    # separate the date
    dateX = datetime.datetime.strptime(dateToChangeTo, '%a %d %B, %Y')

    dateYear = dateX.strftime('%Y')
    dateMonth = dateX.strftime('%b')
    dateDay = dateX.strftime('%d')

    # get Month Values for array to click
    selectingMonth = dateX.strftime('%m')
    selectingMonth = int(selectingMonth) - 1

    # get Day Value for array to click
    selectingDay = int(dateDay) - 1


    # Change year if appropriate
    currentYear = get_element(calendarYearSelected)
    currentYear = currentYear.text
    if (currentYear != dateYear):
        yearToSelectLoc = calendarYearToSelect + str(dateYear) + '"]'

        # select the required year value
        get_element(calendarYearOptions).click()
        get_element(yearToSelectLoc).click()

    # Change Month if appropriate
    currentMonth = get_element(calendarMonthSelected).text
    if (currentMonth != dateMonth):
        monthToSelectLoc = calendarMonthToSelect + str(selectingMonth) + '"]'

        # select the required month value
        get_element(calendarMonthOptions).click()
        get_element(monthToSelectLoc).click()

    # select the day
    cDates = get_elements(calendarAllDates)
    dateWebAddress = cDates[selectingDay]
    dateWebAddress.click()

    return dateWebAddress


def send_browser_key(key: Keys):
    ActionChains(common.browser).send_keys(Keys.ESCAPE).perform()


def is_print_dialog_present(timeout: int=5) -> bool:
    ret = False

    try:
        wait_visibility_of_element('print-preview', By.ID, timeout, 'Waiting for print dialog timed out')
        ret = True
    except TimeoutException:
        pass

    return ret


def get_growl_message():
    wait_visibility_of_element(".growl-message.ng-binding")
    msg = get_element("(//p[@class='growl-message ng-binding'])[1]", by=By.XPATH)

    if msg:
        return msg.text
    else:
        return ''


def get_facet_element(facet: string, value: string):
    """Select a value from a faceted search facet"""
    xpath = "//label[text()='" + facet + "']/following::ul[1]/li[contains(.,'" + value + "')]"
    return get_element(xpath, by=By.XPATH)


def get_drop_down_selected_value(drop_down_id):
    # First strip the '#' if supplied
    drop_down_id = drop_down_id.replace('#', '')
    xpath = "//list[@id='" + drop_down_id + "']/descendant::span[contains(@class,'selected')]"
    element = get_element(xpath, By.XPATH)
    return element.text