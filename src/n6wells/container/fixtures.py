from n6wells.db import *
from n6wells.container.models import ContainerType, Container


PLATE96_NAME = 'Plate-96_well'

def load():
    try:
        typ = ContainerType.uniq_name(PLATE96_NAME)
    except NoResultFound:
        # load fixtures
        conn = get_handle()

        typ = ContainerType(name=PLATE96_NAME)
        ct = 0
        for _row in range(ord('A'),ord('H')+1):
            row = chr(_row)
            for col in range(12):
                wellname = '%s%02d' % (row,col+1)
                conn.add( Container( type=typ, order=ct, name=wellname ) )
                ct += 1
        conn.commit()
