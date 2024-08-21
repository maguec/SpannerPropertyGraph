from dataclass_csv import DataclassWriter
from sys import exit


##########################################################################################
# This is a generic write function
def writecsv(l, c, outfile):
    with open(outfile, "w") as f:
        w = DataclassWriter(f, l.list_items, c)
        w.write()

def typemap(t):
    tmap = {
        "int": "INT64 NOT NULL",
        "str": "STRING(MAX)",
        "Decimal": "NUMERIC",  # https://cloud.google.com/spanner/docs/working-with-numerics
    }
    return tmap[t]


def writeSpanner(transaction, c, batch=1000):
    rows = []
    print("Writing {} to Spanner".format(c.list_items[0].__class__.__name__))
    columns = c.list_items[0].__dataclass_fields__.keys()
    for item in c.list_items:
        #rows.append((item.id, item.name, item.tax_rate, item.postcode))
        rows.append(tuple(item.__dict__.values()))
        if len(rows) % batch == 0:
            try:
                transaction.insert(table=c.list_items[0].__class__.__name__, columns=columns, values=rows)
                print("wrote {} rows".format(len(rows)))
                rows = []
            except:
                exit(1)
    if len(rows) > 0:
        try:
            transaction.insert(table=c.list_items[0].__class__.__name__, columns=columns, values=rows)
            print("wrote {} rows".format(len(rows)))
        except:
            print(rows)
            exit(1)
