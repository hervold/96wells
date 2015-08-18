from n6wells.db import *

class ContainerTyp(BaseModel):
    __tablename__ = 'container_type'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=False, unique=True )
    markup = Column( Text, nullable=True )  # for storage of client properties

class Container(BaseModel):
    __tablename__ = 'container_type'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=False, unique=True )
    typ_id = Column( Integer, ForeignKey(ContainerTyp.pk), nullable=False )
    markup = Column( Text, nullable=True )  # for storage of client properties

    typ = relationship(ContainerTyp, backref='units')
