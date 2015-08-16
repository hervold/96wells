from n6wells import *
from n6wells.db import *

class Well(BaseModel):
    __tablename__ = 'well'
    pk = Column( Integer, primary_key=True, nullable=False)
    plate_id = Column( Integer, ForeignKey(Plate.pk), nullable=False )
    name = Column( String(128), nullable=False, unique=True )
