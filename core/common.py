import datetime
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



    # def __ini_module__():
    #     global site_url
    #     global driver_path
    #     global connection_string
    #     global browser
    #     global checking
    #
    #
    # __ini_module__()