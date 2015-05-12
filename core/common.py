from enum import Enum

site_url = r'http://localhost:88/'

driver_path = r"drivers\chromedriver.exe"
connection_string = ""
browser = None  # webdriver.Chrome(driver_path)
checking = False


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
