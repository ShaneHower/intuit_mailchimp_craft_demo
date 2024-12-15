# Python imports
import unittest

# Internal imports
from core.helper_functions import get_country_abbr


class TestingSuite(unittest.TestCase):

    def test_get_country_abbr(self):
        self.assertEqual(get_country_abbr('France'), 'FRE')
        self.assertEqual(get_country_abbr('Saudi Arabia'), 'SA')
        self.assertEqual(get_country_abbr('United States of America'), 'USOA')
        self.assertEqual(get_country_abbr('Switzerland'), 'SWD')


if __name__ == '__main__':
    unittest.main()
