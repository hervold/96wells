import unittest
import n6wells
from n6wells.db import *
from n6wells.util.test import get_test_config
from n6wells.container import fixtures, Container, ContainerType, ContainerInst
from n6wells.xaction import Xaction
from n6wells.sample import Sample, SampleType, Plating


def create():
    config = get_test_config()
    initdb(config['DB']['engine'])

    from n6wells.db import Sample, SampleType, Plating


    print('!!!!')
    conn = get_handle()
    xaction = Xaction()
    conn.add(xaction)
    typ1, typC = SampleType(name='patient'), SampleType(name='control')
    conn.add(typ1)
    s1, s2 = Sample(sample_type=typ1), Sample(sample_type=typC)
    plate96_t = conn.query(ContainerType).filter(ContainerType.name=='Plate-96_well').one()
    plate = ContainerInst( name='my_plate', type=plate96_t )
    well1 = conn.query(Container).filter(Container.type == plate96_t).filter(Container.name == 'A01').one()
    well2 = conn.query(Container).filter(Container.type == plate96_t).filter(Container.name == 'A02').one()
    print('####')
    p1 = Plating( plate=plate, well=well1, sample=s1, xaction=xaction )
    print('$$$$')
    p2 = Plating( plate=plate, well=well2, sample=s2, xaction=xaction )
    print('^^^')
    conn.add( p1 )
    print('@@@@')
    conn.add( p2 )
    conn.commit()
    print('0000')
    return plate

class SampleTest(unittest.TestCase):
    def setUp(self):
        config = get_test_config()
        initdb(config['DB']['engine'])
        fixtures.load()

    def test(self):
        plate = create()
        print('@@ sample.test - plate: %s :: name=%s, dict: %s' % (plate,plate.name, plate.to_dict( AssocClass=Plating ) ))
