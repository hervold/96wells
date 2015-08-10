from n6wells import *
from n6wells.db import *
from n6wells.db.constants import Meas_Action_Enum
from n6wells.event import Event


class Measurement(BaseModel):
    __tablename__ = 'sample_meas'
    pk = Column( Integer, primary_key=True, nullable=False )
    action = Column( Meas_Action_Enum, nullable=False )
    event_id = Column( Integer, ForeignKey(Event.pk), nullable=False )

    event = relationship(Event)

