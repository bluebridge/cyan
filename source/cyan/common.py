# global site_url
# global driver_path
# global browser
# global connection_string
# global checking
import datetime
from enum import Enum

site_url = r'http://localhost:88/'
driver_path = r"drivers\chromedriver.exe"
# connection_string = "Driver={SQL Server Native Client 10.0};Server=.;Database=cosacsTest;Trusted_Connection=yes;"
connection_string = "Driver={SQL Server Native Client 11.0}; Server=.; Database=cosacs;Trusted_Connection=yes;"
browser = None  # webdriver.Chrome(driver_path)
checking = False
"""
Non Stocks
"""
random_int = (datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
sku = "S%s" % random_int
iupc = "I%s" % random_int
shortt_description = 'SD%s' % random_int
longg_description = 'LD%s' % random_int
link_name = 'Sel%s' % random_int
global promotion_type
firstname = "FN%s" % random_int
lastname = "LN%s" % random_int
homephone = random_int
mobilephone = random_int
username = 99999
password = 'ingres##'


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