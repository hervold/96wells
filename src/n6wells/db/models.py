"""
generic table for linking items together by adding a foreign key to both

basically the equivalent of having everything inherit from a global
parent table, but lighter-weight
"""

from n6wells import *
from n6wells.db import *


class Link(BaseModel):
    __tablename__ = 'link'
    pk = Column( Integer, primary_key=True, nullable=False)
