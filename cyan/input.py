import string
import datetime

from . import dom, security, common

from selenium.webdriver import ActionChains

from selenium.webdriver.remote.webelement import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from .common import ListFilterType

ListCssFilters = {1: "list#%s']",
                  2: "list[ng-model='%s']",
                  3: "list[lookup='%s']",
                  4: "list[placeholder='%s']",
                  5: "list[name='%s']"
                  }


def write_on_textbox(text: string, search_filter: string, by: By=By.CSS_SELECTOR):
    """
    Write on a textbox element.

    :param text: The text to write
    :param search_filter: The element identifier to search by
    :param by: element filter type
    """
    security.check_self()
    element = dom.get_element(search_filter, by)
    write_on_element(text, element)


def write_on_ng_textbox(text: str, model_name: str, element_tag: str='*', angular_prefix: str='ng'):
    """
    Write on a textbox element using Angular model name.

    :param text: The text to write
    :param model_name: Angular model binding name
    :param element_tag: The element's html tag
    :param angular_prefix: angular html data prefix
    :param element_tag: DOM element's tag
    """
    security.check_self()
    element = dom.get_element_by_angular_model(model_name, element_tag, angular_prefix)
    write_on_element(text, element)


def write_on_element(text: string, element: WebElement):
    """

    :rtype : object
    """
    security.check_self()
    dom.validate_element(element)
    element.send_keys(text)


def click_button(button_text: string, tag: str='button'):
    """
    Click on a button by its display text.

    :param button_text: The button's display text
    """
    security.check_self()

    element = dom.get_element_by_text(button_text, tag)
    click_on_element(element)


def click_button_by_id(button_id: string):
    """
    Click on a button by its id.

    :param button_id: The button's id
    """
    security.check_self()
    element = dom.get_element(button_id)
    click_on_element(element)


def fill_textbox_by_label_text(label_text, value_for_textbox,
                               search_type: common.TextSearchType=common.TextSearchType.Exact):
    """
    Write to  a textbox by its label text.

    :param label_text: The textbox' label text
    :param value_for_textbox: The text to write
    """
    security.check_self()

    # //input[@id=(//label[normalize-space(text())='%s']/@for)]
    xpath = common.get_attr_xpath("//input[@id=(//label", "text()", label_text, search_type, "/@for)]")

    text_box = dom.get_element(xpath, By.XPATH)

    assert (text_box is not None), "Cannot find textbox with associated label's text '%s'" % label_text

    text_box.send_keys(value_for_textbox)


def fill_textbox_by_attribute_value(value_to_fill: string, attr_value: string, attr_name: string='@placeholder'):
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


def fill_text_boxes_by_attribute_value(values: dict, attr_name: string='@placeholder'):
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

    selector = "//div[contains(concat(' ',normalize-space(@class),' '),' list-placeholder ')]/span[text()='{0}']/..".format(
        grayed_text)
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


def select2_set_value_filter(value: string, search_filter: string, by: By=By.CSS_SELECTOR):
    """
    :param value: value to set to the select2
    :param search_filter: The element identifier to search by (div expected)
    :param by: element filter type
    """
    security.check_self()

    all_elements = dom.get_elements(search_filter, by)

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


def select_set_value(value: str, search_type: common.TextSearchType=common.TextSearchType.Contain):
    """
    Select a value from a drop down list by passing the string text of that value
    :param value:
    """
    security.check_self()

    xpath = common.get_attr_xpath("//option", "text()", value, search_type)
    option_item = dom.get_element(xpath, By.XPATH)
    option_item.click()


def set_list_value(value: str, list_filter: str, filter_type: ListFilterType=ListFilterType.NgModel,
                   search_type: common.TextSearchType=common.TextSearchType.Contain):
    """
    Select a list item of the 'list' drop-down directive by the passed value
    :param value: The list item value to select
    :param list_filter: The 'list' directive filter value
    :param filter_type: Type of the list filter
    """
    css = ListCssFilters[filter_type.value] % list_filter
    ele = dom.get_element(css)

    if ele:
        arrow_btn = ele.find_element_by_class_name('list-arrow')
        arrow_btn.click()

        if filter_type == ListFilterType.PlaceHolder:
            xpath = "//list[@placeholder='" + list_filter + "']/descendant::div[contains(text(), '" + value + "')][1]"
        else:
            xpath = common.get_attr_xpath("//div", "text()", value)
        list_item = ele.find_element_by_xpath(xpath)
        list_item.click()


def set_select_value_by_text(place_holder_text: string, sel_text:string):
    xpath = "//list[@placeholder='%s']" % place_holder_text
    lst = dom.get_element(xpath, By.XPATH)

    if lst:
        xpath = "//div[contains(text(), '%s')]" % sel_text
        list_item = lst.find_element_by_xpath(xpath)
        if list_item:
            list_item.click()

    else:
        return None


def set_drop_down_value_by_model(ng_model: str, value: str,
                                 search_type: common.TextSearchType = common.TextSearchType.Contain):
    xpath = "//select[@ng-model='%s']/option" % ng_model
    xpath = common.get_attr_xpath_ci(xpath, "@value", value, search_type)
    click_element(xpath, By.XPATH)


def set_drop_down_text_by_model(ng_model: str, value: str,
                                search_type: common.TextSearchType = common.TextSearchType.Contain):
    xpath = "//select[@ng-model='%s']/option" % ng_model
    xpath = common.get_attr_xpath_ci(xpath, "text()", value, search_type)
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


def click_on_span_element(element_to_click: WebElement):
    """
    Perform a click on an element

    :param element_to_click: element to click
    """
    security.check_self()
    # dom.validate_element(element_to_click)
    ActionChains(common.browser).move_to_element(element_to_click).click().perform()


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
        dom.wait_presence_of_element("close", by=By.CLASS_NAME)
        dom.time.sleep(0.5)
        click_element("close", by=By.CLASS_NAME)
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


def add_days(days: int):
    datetime.date.today() + datetime.timedelta(days=days).d.day


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


def clear_select2_by_label(label_text):
    """
    Clicks the little 'x' in a Cosacs drop down based on id
    """
    xpath = "//label[text()='" + label_text + "']/following::i[contains(@class, 'remove')][1]"
    element = dom.get_element(xpath, By.XPATH)
    if element.is_displayed():
        click_on_element(element)

def clear_select2_by_css(search_filter: string, by: By=By.CSS_SELECTOR):
    """
    Clicks the little 'x' in a Cosacs select2 based on a css selector for the select2
    
    :param search_filter: The element identifier to search by
    :param by: Element filter type
    """
    search_filter += ' .remove'
    element = dom.get_element(search_filter, by)
    if element.is_displayed():
        click_on_element(element)
