import unittest
from n6wells.db import *
from n6wells.util.test import get_test_config
from n6wells.container import fixtures, Container, ContainerTyp


class ContainerTest(unittest.TestCase):
    def setUp(self):
        config = get_test_config()
        initdb(config['DB']['engine'])


    def test_cont(self):
        fixtures.load()

        conn = get_handle()
        for typ in conn.query(ContainerTyp):
            for cont in typ.units:
                print('@@ %s :: %s' % (typ, cont))
