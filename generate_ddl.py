#! /usr/bin/env python

from models.nodes import *
from models.edges import *
from models.utils import *

if __name__ == "__main__":
    full_ddl = ["-- Node Tables"]
    counties = Counties()
    full_ddl.append(counties.genddl())  # counties.genddl()
    properties = Properties()
    full_ddl.append(properties.genddl())  # properties.genddl()
    owners = Owners()
    full_ddl.append(owners.genddl())  # owners.genddl()
    credit_reports = CreditReports()
    full_ddl.append(credit_reports.genddl())  # credit_reports.genddl()
    full_ddl.append("-- Edge Tables")
    credit_edges = CreditEdges(owners, credit_reports)
    full_ddl.append(credit_edges.genddl())  # credit_edges.genddl()
    county_edges = CountyEdges(properties, counties)
    full_ddl.append(county_edges.genddl())  # county_edges.genddl()
    property_edges = PropertyEdges(properties, owners)
    full_ddl.append(property_edges.genddl())  # property_edges.genddl()
    full_ddl.append("-- Graph Declaration")
    full_ddl.append("CREATE OR REPLACE PROPERTY GRAPH PropertyGraph")
    full_ddl.append("  NODE TABLES (")
    full_ddl.append(
        "    "
        + ",\n    ".join(
            [
                counties.list_items[0].__class__.__name__,
                properties.list_items[0].__class__.__name__,
                owners.list_items[0].__class__.__name__,
                credit_reports.list_items[0].__class__.__name__,
            ]
        )
    )
    full_ddl.append("  )")
    full_ddl.append("  EDGE TABLES (")
    full_ddl.append("    " + property_edges.gendeclarationddl() + ",")
    full_ddl.append("    " + county_edges.gendeclarationddl()+ ",")
    full_ddl.append("    " + credit_edges.gendeclarationddl())
    full_ddl.append(");")

    print("\n".join(full_ddl))
