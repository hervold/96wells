import n6wells
from n6wells.db import *
from pandas import *
from collections import defaultdict
import string

class Plate(BaseModel):
    def __init__(self, name):
        self.name = name
        d = {}
        self.positions = DataFrame(data=d, index=[str(x) for x in range(1,13)],
                             columns=list(string.ascii_uppercase)[0:8])

    def row(self, row_name):
        return self.positions[:row_name]

    def col(self, col_name):
        return self.positions[str(col_name)]

    def well(self, well_name):
        return self.positions[row_name][col_name]

    def place_well(self, row, col, sample):
        row = str(row)
        col = str(col)
        nd = {col: sample}
        ndf = DataFrame(data=nd, index=[str(row)])
        self.positions.update(ndf)

    def free_wells(self):
        pass

    def num_free_wells(self):
        pass

    def save(self):
        pass

    __tablename__ = 'plate'
    pk = Column( Integer, primary_key=True, nullable=False)
    name = Column( String(128), nullable=False, unique=True )
