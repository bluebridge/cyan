"""
    ---------------------------------------------------------------------

    This module contains the functionality that related to DOM tree like:
        * Finding DOM's elements.
        * Checking the elements state (Present, visible,..etc.)

    ---------------------------------------------------------------------

"""

import string
from http.client import CannotSendRequest
import datetime
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.remote.webelement import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from cyan.core import security, common


def get_browser() -> webdriver.chrome.webdriver.WebDriver:
    """
    Get the shared web driver.

    :return: The web driver
    :rtype: WebDriver
    """
    return common.browser


def wait_for_text_present(text_to_present: string, text_element: string, timer: int=30, by: By=By.ID):
    """
    Wait for a string literal to be present on the page.

    :param text_to_present: The string to wait for its present
    :param text_element: The dom element whose has the string as its value.
    :param timer: Time to wait before it's timeout
    :param by: The string's attribute
    """
    security.check_self()

    wait_visibility_of_element(text_element, timer, by)

    WebDriverWait(common.browser, timeout=10).until(
        element_text_available_callback(text_to_present, text_element, by))


def wait_presence_of_element(search_filter, timer: int=10, by: By=By.ID):
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


def wait_presence_of_element_by_text(element_text: string, timer: int=10):
    """
    Wait for an element to be loaded on the page

    :param element_text: The element text to search by
    :param timer: time to wait before it through a timeout error
    """
    security.check_self()

    xpath = "//.[contains(text(), '%s')]" % element_text
    WebDriverWait(common.browser, timeout=timer).until(
        ec.presence_of_element_located((By.XPATH, xpath))
    )


def element_text_available_callback(element_text: string, element: string, by: By=By.ID):
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


def wait_visibility_of_element(search_filter, timer: int=10, element_by: By=By.ID,
                               msg: string='Waiting for element timed out'):
    """
    Wait for an element to be loaded and become visible on the page.

    :param search_filter: The element identifier to search by
    :param timer: time to wait before it through a timeout error
    :param element_by: element filter type
    """
    security.check_self()
    WebDriverWait(common.browser, timer) \
        .until(lambda s: s.find_element(element_by, search_filter).is_displayed(), msg)


def wait_visibility_of_element_by_text(element_text: string, timer: int=10,
                                       msg: string='Waiting for element timed out'):
    """
    Wait for an element to be loaded and become visible on the page.

    :param element_text: The element's text to search by
    :param timer: time to wait before it through a timeout error
    :param msg: Message to fire when timeout error thrown
    """
    security.check_self()
    xpath = "//.[contains(text(), '%s')]" % element_text

    WebDriverWait(common.browser, timer) \
        .until(lambda s: s.find_element(By.XPATH, xpath).is_displayed(), msg)


def is_element_present(search_filter, element_by: By=By.ID) -> bool:
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


def is_element_visible(search_filter, element_by: By=By.ID) -> bool:
    security.check_self()

    try:
        element = get_element(search_filter, element_by)
        return element.is_displayed()
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False


def is_element_visible_text(element_text: string) -> bool:
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


def is_element_visible_attr(attr_name: string, attr_value: string, tag: string='input') -> bool:
    state = False
    xpath = "//{0}[@{1}='{2}']".format(tag, attr_name, attr_value)
    ele = common.browser.find_elements_by_xpath(xpath)

    if ele:
        state = ele.is_displayed()

    return state


def is_element_disabled(css):
    """
    Checks if the element has the 'disabled' class attached to the element.

    :param css:
    :return:
    """
    css += ' .disabled'

    try:
        we = get_element(css, By.CSS_SELECTOR)
        state = True
    except:
        state = False

    return state


def is_element_selected(search_filter, element_by: By=By.ID) -> bool:
    """
    To check if a tick box is selected.

    :param search_filter:
    :param element_by:
    :return:
    """
    security.check_self()

    try:
        element = get_element(search_filter, element_by)
        return element.is_selected
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False


def is_element_enabled(search_filter, element_by: By=By.ID) -> bool:
    security.check_self()

    try:
        element = get_element(search_filter, element_by)
        return element.is_enabled()
    except NoSuchElementException:
        return False
    except ConnectionRefusedError:
        return False


def select_from_dropdown(xpath: string, selection: string):
    dropdown = get_element(xpath, By.XPATH)
    dropdown.click()
    wait(0.5)

    css = "div.list-item:nth-child(" + selection + ")"  # Select the nth option from the drop down list
    option = get_element(css, By.CSS_SELECTOR)
    option.click()
    wait(0.5)


def select_from_dropdown_search(css: string, selection: string):
    css1 = css + ' .play'
    we = get_elements(css1, By.CSS_SELECTOR)
    we[0].click()  # Open up the entry box

    css2 = css + ' input'
    wait(1)
    we = get_element(css2, By.CSS_SELECTOR)
    we.send_keys(Keys.CONTROL + "a")
    we.send_keys(selection)

    # Now click on the search result
    css3 = css + ' .list-options .list-item'
    wait_presence_of_element(css3, 10, By.CSS_SELECTOR)
    we = get_elements(css3, By.CSS_SELECTOR)
    we[0].click()


def get_Options_from_dropdown_search(css: string):
    options = []

    css1 = css + ' .play'
    wait_presence_of_element(css, 10, By.CSS_SELECTOR)
    we = get_element(css1, By.CSS_SELECTOR)
    we.click()  # Open up the entry box

    css = '.list-options .list-item'
    we = get_elements(css, By.CSS_SELECTOR)
    count = len(we)

    for x in range(0, (count - 1)):
        name = we[x].text
        options.append(name)

    return options


def select_from_dropdown_CSS(css: string, selection: string):
    dropdown = get_element(css, By.CSS_SELECTOR)
    dropdown.click()
    wait(0.5)

    css = "div.list-item:nth-child(" + selection + ")"  # Select the nth option from the drop down list
    option = get_element(css, By.CSS_SELECTOR)
    option.click()
    wait(0.5)


def select_from_add(css, name):
    """
    Enter the 'name' in the search text box then click on 'Enter' to select

    :param css:
    :param name:
    """
    we = get_element(css, By.CSS_SELECTOR)
    input = we.find_element(By.CSS_SELECTOR, 'input')
    input.send_keys(name)
    input.send_keys(Keys.ENTER)

    # Now click on the 'Add'
    we = get_element(css, By.CSS_SELECTOR)
    add = we.find_element(By.CSS_SELECTOR, 'button')
    add.click()


def select_from_dropdown_no_search(css: string, selection: string):
    dropdown = get_element(css, By.CSS_SELECTOR)

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


def get_element(search_filter: string, by: By=By.ID) -> WebElement:
    """
    Get an element by its identifier.

    :param search_filter: The element identifier to search by
    :param by: Element's filter type
    :return:
    :rtype: WebElement
    """
    security.check_self()
    return common.browser.find_element(by, search_filter)


def get_element_by_value(value: string) -> WebElement:
    """
    Get DOM element by its value.

    :param value: Element's value
    :return: The element
    """

    xpath = "//*[contains(value(), '%s')]" % value
    return common.browser.find_elements_by_xpath(xpath)


def get_element_by_text(value: string, search_type: common.TextSearchType=common.TextSearchType.Contain) -> WebElement:
    """
    Get DOM element by its text.

    :param value:
    :param search_type:
    :return:
    """
    options = {1: "//*[normalize-space(text())='%s']",
               2: "//*[starts-with(text(), '%s')]",
               3: "//*[ends-with(text(), '%s')]",
               4: "//*[contains(text(), '%s')]"
               }
    xpath = options[search_type.value] % value
    ele = get_element(xpath, By.XPATH)

    if ele:
        return ele
    else:
        return None


def get_element_by_angular_model(model_name: str, element_tag: str='*', angular_prefix: str='ng') -> WebElement:
    """
    Get DOM element by its AngularJs model's binding.

    :param model_name: Angular model binding name
    :param element_tag: The element's html tag
    :param angular_prefix: angular html data prefix
    :return: The element
    """

    xpath = "//%s[@%s-model='%s']" % (element_tag, angular_prefix, model_name)
    return common.browser.find_elements_by_xpath(xpath)


def get_elements(search_filter: string, by: By=By.ID):
    """
    Get all element by its identifier.

    :param search_filter: The elements identifier to search by
    :param by: element filter type
    :return:
    """
    security.check_self()

    return common.browser.find_elements(by, search_filter)


def get_label_by_partial_text(label_text: string) -> WebElement:
    """
    Get a label by its partial text.

    :param label_text: label's partial text
    :return: The found label as WebElement
    """
    xpath = "//label[contains(.,'%s')]/.." % label_text
    return get_element(xpath, By.XPATH)


def get_label_by_text(label_text: string) -> WebElement:
    """
    Get a label by its text.

    :param label_text: label's text
    :return: The found label as WebElement
    """
    xpath = "//label[normalize-space(text())= '%s']" % label_text
    return get_element(xpath, By.XPATH)


def get_link_by_text(link_text: string) -> WebElement:
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


def wait(timer):
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


def scroll_down():
    security.check_self()
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scrolldown():
    security.check_self()
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    common.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scrolldownOne():
    security.check_self()
    common.browser.execute_script("window.scrollBy(0,7800)", "")


def scroll_element_to_view_1(element_name):
    start = 0
    end = 200
    for permission_displayed in get_elements("table."
                                             "table:nth-child(n) > tbody:nth-child(2) > tr:nth-child(n) > "
                                             "td:nth-child(1)", By.CSS_SELECTOR):
        exp = permission_displayed.text
        if element_name in permission_displayed.text:
            wait(2)
            break
        else:
            security.check_self()
            common.browser.execute_script("scroll(%s, %s);" % (start, end))
            start = end
            end += 48


def scroll_down_100():
    security.check_self()
    common.browser.execute_script("window.scrollBy(0, 100)")


#
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


def scrollup(distance):
    security.check_self()
    text = "window.scrollBy(0,-" + distance + ")"
    common.browser.execute_script(text, "")


def scroll_element_into_view(elementWe):
    y = elementWe.location['y'] - 50
    common.browser.execute_script('window.scrollTo(0, {0})'.format(y))
    wait(0.5)


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
    currentYear = get_element(calendarYearSelected, By.CSS_SELECTOR)
    currentYear = currentYear.text
    if (currentYear != dateYear):
        yearToSelectLoc = calendarYearToSelect + str(dateYear) + '"]'

        # select the required year value
        get_element(calendarYearOptions, By.CSS_SELECTOR).click()
        get_element(yearToSelectLoc, By.CSS_SELECTOR).click()

    # Change Month if appropriate
    currentMonth = get_element(calendarMonthSelected, By.CSS_SELECTOR).text
    if (currentMonth != dateMonth):
        monthToSelectLoc = calendarMonthToSelect + str(selectingMonth) + '"]'

        # select the required month value
        get_element(calendarMonthOptions, By.CSS_SELECTOR).click()
        get_element(monthToSelectLoc, By.CSS_SELECTOR).click()

    # select the day
    cDates = get_elements(calendarAllDates, By.CSS_SELECTOR)
    dateWebAddress = cDates[selectingDay]
    dateWebAddress.click()

    return dateWebAddress


# small modification on the module above to throw an exception if the date specified is not settable
def click_Calendar_djc(dateToChangeTo):
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
    calendarAllDates = 'td:not(.ui-state-disabled) .ui-state-default'  # Will only return enabled days


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
    currentYear = get_element(calendarYearSelected, By.CSS_SELECTOR)
    currentYear = currentYear.text
    if (currentYear != dateYear):
        yearToSelectLoc = calendarYearToSelect + str(dateYear) + '"]'

        # select the required year value
        get_element(calendarYearOptions, By.CSS_SELECTOR).click()
        get_element(yearToSelectLoc, By.CSS_SELECTOR).click()

    # Change Month if appropriate
    currentMonth = get_element(calendarMonthSelected, By.CSS_SELECTOR).text
    if (currentMonth != dateMonth):
        monthToSelectLoc = calendarMonthToSelect + str(selectingMonth) + '"]'

        # select the required month value
        get_element(calendarMonthOptions, By.CSS_SELECTOR).click()
        get_element(monthToSelectLoc, By.CSS_SELECTOR).click()

    # select the day
    cDates = get_elements(calendarAllDates, By.CSS_SELECTOR)
    count = len(cDates)
    if count < selectingDay:
        raise ValueError("Day not selectable")
    else:
        dateWebAddress = cDates[selectingDay]
        dateWebAddress.click()

        return dateWebAddress


def list_compare(list1, list2):
    """
    Compare the two lists nd return True if they are the same otherwise return False.

    :param list1:
    :param list2:
    :return:
    """
    count1 = len(list1)
    count2 = len(list2)
    result = True
    if count1 != count2:
        result = False
    else:
        x = []  # Convert list1 to uppercase
        for a in list1:
            x.append(a.upper())
        x.sort()
        y = []  # Convert list2 to uppercase
        for a in list1:
            y.append(a.upper())
        y.sort()
        if x == y:  # See if they are the same
            result = True
        else:
            result = False

    return result


def send_browser_key(key: Keys):
    ActionChains(common.browser).send_keys(Keys.ESCAPE).perform()


def is_print_dialog_present(timeout: int=5) -> bool:
    ret = False

    try:
        wait_visibility_of_element('print-preview', timeout, By.ID, 'Waiting for print dialog timed out')
        ret = True
    except TimeoutException:
        pass

    return ret