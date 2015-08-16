import unittest
import n6wells
from n6wells.db import *
from n6wells.util.test import get_test_config


class SampleTest(unittest.TestCase):
    def setUp(self):
        config = get_test_config()
        initdb(config['DB']['engine'])


    def test(self):
        pass
