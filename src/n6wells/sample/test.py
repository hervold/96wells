import unittest
import n6wells
from n6wells.db import *
from n6wells.util.test import get_test_config
from n6wells.container import fixtures, ContainerInst
from n6wells.xaction import Xaction
from n6wells.sample import Sample, SampleType, Plating


class SampleTest(unittest.TestCase):
    def setUp(self):
        config = get_test_config()
        initdb(config['DB']['engine'])
        fixtures.load()

    def test(self):
        conn = get_handle()
        xaction = Xaction()
        typ1, typC = SampleType(name='patient'), SampleType(name='control')
        s1, s2 = Sample(sample_type=typ1), Sample(sample_type=typC)
        plate = ContainerInst()
        plate96_t = conn.query(ContainerTyp).filter(ContainerTyp.name=='Plate-96_well').one()
        well1 = conn.query(Container).filter(typ==plate96, name='A01').one()
        well2 = conn.query(Container).filter(typ==plate96, name='A02').one()
        p1 = Plating( plate=plate, well=well1, sample=s1, xaction=xaction )
        p2 = Plating( plate=plate, well=well2, sample=s2, xaction=xaction )
