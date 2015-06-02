import unittest
from cyan.core import nav


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        nav.quit_browser()