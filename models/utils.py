from dataclass_csv import DataclassWriter
from sys import exit
from faker import Faker

fake = Faker()


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
        "list": "ARRAY<FLOAT64>(vector_length=>768) NOT NULL",  # https://cloud.google.com/spanner/docs/arrays
    }
    return tmap[t]


def writeSpanner(transaction, c, batch=1000, debug=False):
    rows = []
    print("Writing {} to Spanner".format(c.list_items[0].__class__.__name__))
    columns = c.list_items[0].__dataclass_fields__.keys()
    if debug:
        print(columns)
    for item in c.list_items:
        rows.append(tuple(item.__dict__.values()))
        if debug:
            print(tuple(item.__dict__.values()))
        if len(rows) % batch == 0:
            try:
                transaction.insert(
                    table=c.list_items[0].__class__.__name__,
                    columns=columns,
                    values=rows,
                )
                print("wrote {} rows".format(len(rows)))
                rows = []
            except:
                exit(1)
    if len(rows) > 0:
        try:
            transaction.insert(
                table=c.list_items[0].__class__.__name__, columns=columns, values=rows
            )
            print("wrote {} rows".format(len(rows)))
        except:
            print(rows)
            exit(1)


def oneToManyGen(srcLen, destLen, theRandom):
    conns = []
    for i in range(0, srcLen - 1):
        for j in range(0, fake.random_int(min=1, max=theRandom)):
            while True:
                dest = fake.random_int(min=0, max=destLen - 1)
                if dest != i:
                    conns.append((i, dest))
                    break
    return list(set(conns))  # use a set to ensure unique relationships
