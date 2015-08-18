from n6wells.db import *
from n6wells.db.models import Link


class ContainerTyp(BaseModel):
    """
    used to group "slots" into one container, eg, wells into a plate
    """
    __tablename__ = 'container_type'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=False, unique=True )
    markup = Column( Text, nullable=True )  # for storage of client properties


class Container(BaseModel):
    """
    the bit that actually holds something (eg, a well)
    """
    __tablename__ = 'container'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=False, unique=True )
    order = Column( Integer, nullable=False )
    typ_id = Column( Integer, ForeignKey(ContainerTyp.pk), nullable=False )
    markup = Column( Text, nullable=True )  # for storage of client properties

    typ = relationship(ContainerTyp, backref='units')

    __table_args__ = (
        UniqueConstraint('order','typ_id'),
    )


class ContainerInst(BaseModel):
    """
    individual container instances, eg, one specific plate
    """
    __tablename__ = 'container_instance'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=True, unique=True )
    typ_id = Column( Integer, ForeignKey(ContainerTyp.pk), nullable=False )
    link_id = Column( Integer, ForeignKey(Link.pk), nullable=False )
    created = Column(DateTime, default=sql_func.now(), nullable=False )

    link = relationship(Link)
    typ = relationship(ContainerTyp)
