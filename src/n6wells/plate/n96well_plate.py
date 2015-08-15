from n6wells import *
from n6wells.db import *
from collections import defaultdict

class Plate(BaseModel):
    def __init__(self, name):
        self.name = name
        self.positions = positions = DataFrame(data=d, index=[x for x in range(1,13)],
                             columns=list(string.ascii_lowercase)[0:8])

    def row(self, row_name):
        return self.positions[:row_name]

    def col(self, col_name):
        return self.positions[col_name]

    def place_well(self, row, col, sample):
        nd = {col: sample}
        ndf = DataFrame(data=nd, index=[row])
        self.positions.update(df2)

    def free_wells(self):
        pass

    def num_free_wells(self):
        pass

    def save(self):
        pass

    __tablename__ = 'plate'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=False, unique=True )
