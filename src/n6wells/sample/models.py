from n6wells import *
from n6wells.db import *
from n6wells.db.models import Link
from n6wells.xaction import Xaction
from n6wells.container import ContainerType, Container, ContainerInst



class SampleType(BaseModel):
    __tablename__ = 'sample_type'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=False, unique=True )
    created = Column(DateTime, default=sql_func.now(), nullable=False )


class Sample(BaseModel):
    __tablename__ = 'sample'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=True, unique=True )
    sample_type_pk = Column( Integer, ForeignKey(SampleType.pk), nullable=False )
    link_pk = Column( Integer, ForeignKey(Link.pk), nullable=False )
    created = Column(DateTime, default=sql_func.now(), nullable=False )

    sample_type = relationship(SampleType)
    link = relationship(Link)
    __mapper_args__ = {'polymorphic_on': sample_type_pk}

    def __init__(self, *args, **kwargs):
        kwargs['link'] = Link()
        super(Sample,self).__init__(*args, **kwargs)


class Plating(BaseModel):
    __tablename__ = 'plating'
    pk = Column( Integer, primary_key=True, nullable=False)
    container_inst_pk = Column( Integer, ForeignKey(ContainerInst.pk), nullable=False )
    well_pk = Column( Integer, ForeignKey(Container.pk), nullable=False )
    sample_pk = Column( Integer, ForeignKey(Sample.pk), nullable=False )
    xaction_id = Column( Integer, ForeignKey(Xaction.pk), nullable=False )

    container_inst = relationship(ContainerInst)
    plate = synonym('container_inst')
    well = relationship(Container)
    sample = relationship(Sample)
    xaction = relationship(Xaction)

