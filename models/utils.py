from dataclass_csv import DataclassWriter


##########################################################################################
# This is a generic write function
def writecsv(l, c, outfile):
    with open(outfile, "w") as f:
        w = DataclassWriter(f, l.list_items, c)
        w.write()
