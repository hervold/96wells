from n6wells import *
from n6wells.db import *
from n6wells.db.models import Link


class SampleType(BaseModel):
    __tablename__ = 'sample_type'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=False, unique=True )
    created = Column(DateTime, default=sql_func.now(), nullable=False )

class Sample(BaseModel):
    __tablename__ = 'sample'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=True, unique=True )
    sample_type_id = Column( Integer, ForeignKey(SampleType.pk), nullable=False )
    link_id = Column( Integer, ForeignKey(Link.pk), nullable=False )
    created = Column(DateTime, default=sql_func.now(), nullable=False )

    sample_type = relationship(SampleType)
    link = relationship(Link)
    __mapper_args__ = {'polymorphic_on': sample_type_id}

    def __init__(self, *args, **kwargs):
        self.link = Link()
        super(Sample,self).__init__(*args, **kwargs)
