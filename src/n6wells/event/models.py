from n6wells import *
from n6wells.db import *

class Event(BaseModel):
    __tablename__ = 'event'
    pk = Column( Integer, primary_key=True, nullable=False)
