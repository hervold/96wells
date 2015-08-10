
import argparse
from configparser import ConfigParser

def cmdline():
    """
    parse command line options to get config file
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-c','--config', default='/etc/n6wells/settings.ini',
                        help='name of config file')
    args = parser.parse_args()
    config = ConfigParser()
    config.read( args.config )
    return config

    ENGINE_NAME = config['DB']['engine']
