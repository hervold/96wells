
import os
import sys
from configparser import ConfigParser
from n6wells.db import *
from n6wells.container import fixtures
from n6wells.xaction import Xaction
from n6wells.sample import Sample, SampleType, Plating
from n6wells.container import ContainerType, Container, ContainerInst
from configparser import ConfigParser


def get_config():
    fname = os.path.join( os.path.dirname( sys.modules[__name__].__file__ ), 'intgrtest.ini')
    config = ConfigParser()
    config.read( fname )
    return config


@committer
def populate_plate(db):
    xaction = Xaction()
    db.add(xaction)
    db.commit()
    typ1, typC = SampleType(name='patient'), SampleType(name='control')
    s1, s2 = Sample(sample_type=typ1), Sample(sample_type=typC)
    plate96_t = db.query(ContainerType).filter(ContainerType.name=='Plate-96_well').one()
    plate = ContainerInst( name='my_plate', type=plate96_t )
    db.add(plate)
    db.commit()

    well1 = db.query(Container).filter(Container.type == plate96_t).filter(Container.name == 'A01').one()
    well2 = db.query(Container).filter(Container.type == plate96_t).filter(Container.name == 'A02').one()
    p1 = Plating( plate=plate, well=well1, sample=s1, xaction=xaction )
    p2 = Plating( plate=plate, well=well2, sample=s2, xaction=xaction )
    db.add( p1 )
    db.add( p2 )


def main():
    print('@@ helper main')
    config = get_config()
    destroydb(config['DB']['engine'])
    initdb(config['DB']['engine'])
    DB << fixtures.load()
    DB << populate_plate()

