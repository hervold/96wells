import n6wells
from n6wells.plate import Plate
import csv
import argparse

class Importer():

    def __init__(self):
        pass

    def read_plate_from_file(self, fpath):
        plates = {}
        f = csv.DictReader(open(fpath, 'rb'), delimiter='\t', quotechar='"')
        for line in f:
            pname = line['Plate']
            well = line['Well']
            sample = line['Sample']
            col = well[0]
            row = well[1]
            if not pname in plates.keys():
                plates[pname] = Plate(pname)
            plate = plates[pname]
            plate.place_well(row, col, sample)

def _main():
    parser = argparse.ArgumentParser(description='Imports plate')
    parser.add_argument('-f', '--file', help='import help')
    args = parser.parse_args()
    filepath = str(args.file)
    plate_import = Importer()
    plate_import.read_plate_from_file(filepath)

if __name__ == "__main__":
    _main()
