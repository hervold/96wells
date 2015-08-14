from n6wells import *
from n6wells.db import *
from n6wells.db.models import Link
from n6wells.db.constants import Meas_Action_Enum
from n6wells.xaction import Xaction
#from n6wells.db import Xaction


class Measurement(BaseModel):
    __tablename__ = 'sample_meas'
    pk = Column( Integer, primary_key=True, nullable=False )
    action = Column( Meas_Action_Enum, nullable=False )
    xaction_id = Column( Integer, ForeignKey(Xaction.pk), nullable=False )
    link_target_id = Column( Integer, ForeignKey(Link.pk), nullable=False )
    created = Column(DateTime, default=sql_func.now(), nullable=False )

    xaction = relationship('Xaction')
    link_target = relationship(Link)

    @classmethod
    def calc(cls, model, obj):
        conn = get_handle()
        print('@@ desc:', sql_func.desc)
        latest_xaction = conn.query(cls.xaction_id) \
                           .filter( cls.link_target == obj.link ) \
                           .order_by( cls.created.desc() ) \
                           .first()
        print('@@ event:', latest_xaction)
