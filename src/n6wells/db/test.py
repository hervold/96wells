
import unittest
import n6wells
from n6wells.db import *
from n6wells.util.test import get_test_config


class DbTest(unittest.TestCase):
    def setUp(self):
        config = get_test_config()
        initdb(config['DB']['engine'])


    def test_db(self):
        from n6wells.db import Sample, SampleType

        conn = get_handle()
        print( 'before:', conn.query(Sample).all() )

        typ = SampleType(name='TestType')
        print( 'during:', typ)

        s = Sample(sample_type=typ)
        conn.add(s)
        conn.commit()
        [sample] = conn.query(Sample).all()
        print( 'after:', sample )
        print( sample.pk )
        print( Sample.uniq_pk(sample.pk) )
        print('@@ dict:', sample.to_dict() )
        print('@@ type:', sample.sample_type )

