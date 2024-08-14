#! /usr/bin/env python

from models.nodes import *
from models.utils import *

if __name__ == "__main__":
    owners = Owners()
    counties = Counties()
    properties = Properties(items=100)
    credit_reports = CreditReports(items=10000)
    writecsv(credit_reports, CreditReport, "credit_reports.csv")
    writecsv(owners, Owner, "owners.csv")
    writecsv(properties, Property, "properties.csv")
    writecsv(counties, County, "counties.csv")
