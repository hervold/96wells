import os
import os.path
import n6wells
from configparser import ConfigParser


def get_test_config():
    fname = os.path.join( os.path.dirname( n6wells.__file__ ), 'unittest.ini')
    config = ConfigParser()
    config.read( fname )
    return config
