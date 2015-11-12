from enum import Enum

site_url = r'http://localhost:88/'

driver_path = r"drivers\chromedriver.exe"
connection_string = ""
browser = None  # webdriver.Chrome(driver_path)
checking = False
indexing = False

class TextSearchType(Enum):
    Exact = 1
    Start_with = 2
    End_with = 3  # Not Supported in XPath 1.0, Use 'Contains'
    Contain = 4


class ListFilterType(Enum):
    Id = 1
    NgModel = 2
    Lookup = 3
    PlaceHolder = 4
    Name = 5


def get_attr_xpath(prefix: str, attr_name: str, attr_value: str, search_type: TextSearchType=TextSearchType.Contain,
                   suffix: str=""):
    options = {1: "%s[normalize-space(%s)='%s']%s",
               2: "%s[starts-with(%s, '%s')]%s",
               3: "%s[ends-with(%s, '%s')]%s",  # Not Supported in XPath 1.0, Use 'Contains'
               4: "%s[contains(%s, '%s')]%s"
               }

    return options[search_type.value] % (prefix, attr_name, attr_value, suffix)