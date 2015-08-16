import unittest
import n6wells
from n6wells.db import *
from n6wells.util.test import get_test_config


class MeasTest(unittest.TestCase):
    def setUp(self):
        config = get_test_config()
        initdb(config['DB']['engine'])


    def test_meas(self):
        print('@@ running meaurement test!!!')
        from n6wells.sample import Sample, SampleType
        #from n6wells.db import Sample, SampleType, Measurement
        from . import Measurement
        from n6wells.xaction import Xaction

        st = SampleType(name='test_meas')
        s = Sample(sample_type = st)
        x = Xaction()
        print('@@ x:', x)
        m = Measurement( action='measurement', xaction=x, link_target=s.link)
        print('@@', m)

        conn = get_handle()
        conn.add(m)
        conn.commit()

        print('@@ back-query:', Measurement.calc(Sample,s))

        print('@@', conn.query(Measurement).all())
