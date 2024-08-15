#! /usr/bin/env python

from models.nodes import *
from models.edges import *
from models.utils import *

if __name__ == "__main__":
    full_ddl = []
    counties = Counties()
    full_ddl.append(counties.genddl())  # counties.genddl()
    properties = Properties()
    full_ddl.append(properties.genddl())  # properties.genddl()
    owners = Owners()
    full_ddl.append(owners.genddl())  # owners.genddl()
    credit_reports = CreditReports()
    full_ddl.append(credit_reports.genddl())  # credit_reports.genddl()

    print("\n".join(full_ddl))
