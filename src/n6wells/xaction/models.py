from n6wells import *
from n6wells.db import *

class Xaction(BaseModel):
    __tablename__ = 'event'
    pk = Column( Integer, primary_key=True, nullable=False)
    created = Column(DateTime, default=sql_func.now(), nullable=False )
