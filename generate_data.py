#! /usr/bin/env python

from models.nodes import *
from models.edges import *
from models.utils import *

if __name__ == "__main__":
    owners = Owners(items=100)
    counties = Counties(items=40)
    properties = Properties(items=200)
    credit_reports = CreditReports(items=len(owners.list_items))
    writecsv(credit_reports, CreditReport, "credit_reports.csv")
    writecsv(owners, Owner, "owners.csv")
    writecsv(properties, Property, "properties.csv")
    writecsv(counties, County, "counties.csv")
    in_county = CountyEdges(properties, counties)
    writecsv(in_county, InCounty, "in_county.csv")
    has_owner = PropertyEdges(properties, owners)
    writecsv(has_owner, HasOwner, "has_owner.csv")
    has_credit = CreditEdges(owners, credit_reports)
    writecsv(has_credit, HasCreditReport, "has_credit.csv")
