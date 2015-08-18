from n6wells.db import *
from n6wells.container.models import ContainerTyp, Container


def load():
    try:
        typ = ContainerTyp.uniq_name('')
    except NoResultFound:
        # load fixtures
        conn = get_handle()

        typ = ContainerTyp(name='Plate-96_well')
        for _row in range(ord('A'),ord('H')+1):
            row = chr(_row)
            for col in range(12):
                wellname = '%s%02d' % (row,col+1)
                conn.add( Container( typ=typ, name=wellname ) )
        conn.commit()

