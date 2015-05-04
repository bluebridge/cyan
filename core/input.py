import string
import datetime

from cyan.core import dom, security, common

from selenium.webdriver import ActionChains

from selenium.webdriver.remote.webelement import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *


def write_on_textbox(text: string, search_filter: string, by: By=By.CSS_SELECTOR):
    """
    Write on a textbox element.

    :param text: The text to write
    :param search_filter: The element identifier to search by
    :param by: element filter type
    """
    security.check_self()
    element = dom.get_element(search_filter, by)
    dom.validate_element(element)
    element.send_keys(text)


def write_on_element(text: string, element: WebElement):
    """

    :rtype : object
    """
    security.check_self()
    dom.validate_element(element)
    element.send_keys(text)


def click_button(button_text: string):
    """
    Click on a button by its display text.

    :param button_text: The button's display text
    """
    security.check_self()

    element = dom.get_element_by_text(button_text)
    click_on_element(element)


def click_button_by_id(button_id: string):
    """
    Click on a button by its id.

    :param button_id: The button's id
    """
    security.check_self()
    element = dom.get_element(button_id)
    click_on_element(element)


def fill_textbox_by_label_text(label_text, value_for_textbox):
    """
    Write to  a textbox by its label text.

    :param label_text: The textbox' label text
    :param value_for_textbox: The text to write
    """
    security.check_self()
    # xpath = "//label[contains(.,'%s')]" % label_text
    # label = dom.get_element(xpath, By.XPATH)
    xpath = "//input[@id=(//label[normalize-space(text())='%s']/@for)]" % label_text

    text_box = dom.get_element(xpath, By.XPATH)

    assert (text_box is not None), "Cannot find textbox with associated label's text '%s'" % label_text

    text_box.send_keys(value_for_textbox)


def fill_textbox_by_attribute_value(value_to_fill: string, attr_value: string, attr_name: string='placeholder'):
    """
    Write to  a textbox by its attribute value.

    :param value_to_fill: Text to write into the text box
    :param attr_value: Which attribute value to filter with
    :param attr_name: the attribute name
    """
    security.check_self()

    text_box = dom.get_element_by_attribute(attr_name, attr_value, 'input')

    assert (text_box is not None), "Cannot find textbox with attribute '%s' with value '%s'" % (attr_name, attr_value)

    text_box.send_keys(value_to_fill)


def fill_text_boxes_by_labels_text(labels):
    """
    Write to  a series of textbox by tier label texts.

    :param labels: The textbox' label texts
    """
    security.check_self()
    for label, textbox in labels.items():
        fill_textbox_by_label_text(label, textbox)


        # we should com this the function and the select2_set_value together
        # it is not logic to have to functions for this


def fill_text_boxes_by_attribute_value(values: dict, attr_name: string='placeholder'):
    """
    Write to  a series of textbox by trier attribute values.

    :param values: Dictionary of 'attribute values' with corresponded text to write
    :param attr_name: The attribute name to filter with
    """
    security.check_self()
    for attr_value, textbox in values.items():
        fill_textbox_by_attribute_value(textbox, attr_value, attr_name)


def select2_set_value(grayed_text: string, value: string):
    """

    :param grayed_text: the grayed text inside the select2.
    :param value: value to set to the select2
    """
    security.check_self()

    selector = "//a/span[contains(.,'{0}')]/..".format(grayed_text)
    all_elements = dom.get_elements(selector, By.XPATH)

    all_visible = list(filter(lambda i: i.is_displayed(), all_elements))
    # element_found = len(all_visible) == 1

    # assert (element_found, "Can not set text for multiple visible select")

    all_visible[0].click()
    selector = ".select2-drop-active > div > input"
    txt = dom.get_element(selector)
    txt.send_keys(value)
    dom.wait(0.5)
    selector = ".select2-highlighted"
    click_element(selector)


def select2_set_value_ex(grayed_text: string, value: string):
    """

    :param grayed_text: the grayed text inside the BlueBridge select2
    :param value: value to set to the select2
    """
    security.check_self()

    selector = "//span[contains(.,'{0}')]/..".format(grayed_text)
    all_elements = dom.get_elements(selector, By.XPATH)

    all_visible = list(filter(lambda i: i.is_displayed(), all_elements))
    element_found = (len(all_visible) == 1)
    print(all_visible)
    assert element_found, "Can not set text for multiple visible select"

    all_visible[0].click()
    selector = "div.list-options.ng-scope > div > input"
    txt = dom.get_element(selector)
    txt.send_keys(value)
    selector = "div.list-options.ng-scope > div.list-item-container.ng-scope > div.list-item.ng-scope.ng-binding"
    click_element(selector)


def set_select_value_by_text(place_holder_text: string, sel_text:string):
    xpath = "//list[@placeholder='%s']" % place_holder_text
    lst = dom.get_element(xpath, By.XPATH)

    if lst:
        print(lst)
        xpath = "//div[contains(text(), '%s')]" % sel_text
        list_item = lst.find_element_by_xpath(xpath)
        if list_item:
            print(list_item)
            list_item.click()

    else:
        return None


def set_value_by_value(ng_model: string, value: string):
    xpath = "//select[@ng-model='%s']/option[@value='%s']" % (ng_model, value)
    click_element(xpath, By.XPATH)


def set_value_by_text(ng_model: string, text: string):
    xpath = "//select[@ng-model='%s']/option[text()='%s']" % (ng_model, text)
    click_element(xpath, By.XPATH)


def clear_textbox(textbox_filter: string, by: By=By.CSS_SELECTOR, submit: bool=True):
    security.check_self()
    textbox = dom.get_element(textbox_filter, by)
    dom.validate_element(textbox)
    textbox.clear()

    if submit:
        write_on_element(Keys.ENTER, textbox)


def click_element(search_filter: string, by: By=By.CSS_SELECTOR):
    """
    Click on element.

    :rtype : object
    :param search_filter: The element identifier to search by
    :param by: element filter type
    """
    security.check_self()
    element = dom.get_element(search_filter, by)
    click_on_element(element)


def click_on_element(element_to_click: WebElement):
    """
    Perform a click on an element

    :param element_to_click: element to click
    """
    security.check_self()
    # dom.validate_element(element_to_click)
    element_to_click.click()


def hover_on_element(element_to_hover: WebElement):
    security.check_self()
    # assert (element_to_hover is not None)
    # assert element_to_hover.is_displayed() is True, "element is not displayed on the page"
    ActionChains(common.browser).move_to_element(element_to_hover).perform()


def check_notification(message: string):
    """

    :param message:
    """
    security.check_self()

    dom.wait_for_text_present(message, 'navbar', by=By.CLASS_NAME)


def close_notification():
    try:
        security.check_self()
        dom.wait_presence_of_element("growlstatus-close", by=By.CLASS_NAME)
        click_element("growlstatus-close", by=By.CLASS_NAME)
        dom.time.sleep(1)
    finally:
        pass


def focus_on_element(search_filter: string, by: By=By.CSS_SELECTOR):
    element = dom.get_element(search_filter, by)
    focus_on_element(element)


def focus_on_element(element_to_focus: WebElement):
    dom.validate_element(element_to_focus)
    element_to_focus.send_keys(Keys.NULL)


def radio_button_select_value(radio_button_tag: string):
    dom.get_element("input[type='radio'][value='" + radio_button_tag + "']").click()


def get_today_date():
    d = datetime.date.today()
    return d.day


def get_after_days(days: int):
    d = datetime.date.today() + datetime.timedelta(days=days)
    return d.day


def get_tomorrow_date():
    d = datetime.date.today() + datetime.timedelta(days=1)
    return d.day


def select_today_date():
    click_on_element(dom.get_element(str(get_today_date()), By.LINK_TEXT))


def select_tomorrow_date():
    click_on_element(dom.get_element(str(get_tomorrow_date()), By.LINK_TEXT))


def get_day_after_tomorrow():
    d = datetime.date.today() + datetime.timedelta(days=2)
    return d.day


def select_day_after_tomorrow_date():
    click_on_element(dom.get_element(str(get_day_after_tomorrow()), By.LINK_TEXT))


def get_after_3days():
    d = datetime.date.today() + datetime.timedelta(days=3)
    return d.day


def select_after_3days():
    click_on_element(dom.get_element(str(get_after_3days()), By.LINK_TEXT))


def get_element_attribute(search_filter: string, attribute: string, by: By=By.CSS_SELECTOR) -> string:
    """
    Get an element's attribute value by its identifier.

    :rtype : object
    :param search_filter: The element identifier to search by
    :param attribute: the target attribute name
    :param by: element filter type
    :return:
    """
    security.check_self()
    ele = dom.get_element(search_filter, by)
    return ele.get_attribute(attribute)


def get_element_value(search_filter: string, by: By=By.CSS_SELECTOR) -> string:
    """
    Get an element's value by its identifier.

    :rtype : object
    :param search_filter: The element identifier to search by
    :param by: element filter type
    :return:
    """
    security.check_self()
    return get_element_attribute(search_filter, 'value', by)