import unittest
import n6wells
from n6wells.db import *
from n6wells.util.test import get_test_config
from n6wells.container import fixtures, Container, ContainerType, ContainerInst
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
        plate96_t = conn.query(ContainerType).filter(ContainerType.name=='Plate-96_well').one()
        plate = ContainerInst( name='my_plate', type=plate96_t )
        well1 = conn.query(Container).filter(Container.type == plate96_t).filter(Container.name == 'A01').one()
        well2 = conn.query(Container).filter(Container.type == plate96_t).filter(Container.name == 'A02').one()
        p1 = Plating( plate=plate, well=well1, sample=s1, xaction=xaction )
        p2 = Plating( plate=plate, well=well2, sample=s2, xaction=xaction )
        conn.add( p1 )
        conn.add( p2 )
        conn.commit()

        print('@@ sample.test - plate: %s :: name=%s, dict: %s' % (plate,plate.name, plate.to_dict( AssocClass=Plating ) ))
        print('@@ plate96_t.units:', type(plate96_t.units))
