from n6wells import *
from n6wells.db import *


class SampleType(BaseModel):
    __tablename__ = 'sample_type'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=False, unique=True )


class Sample(BaseModel):
    __tablename__ = 'sample'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=True, unique=True )
    sample_type_id = Column( Integer, ForeignKey(SampleType.pk), nullable=False )

    sample_type = relationship(SampleType)
    __mapper_args__ = {'polymorphic_on': sample_type_id}


