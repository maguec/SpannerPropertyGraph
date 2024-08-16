#! /usr/bin/env python

from dataclasses import dataclass
from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker
from Jinja2 import Template

fake = Faker()

EDGE_TABLE_DDL_TEMPLATE = Template(
    """
CREATE TABLE {{name}} (
    {% for field in fields -%}
    {{field}},
    {% endfor -%}
  FOREIGN KEY ({{fkid}}) REFERENCES Account (id)
) PRIMARY KEY (id, {{fkid}}),
  INTERLEAVE IN PARENT {{parent}} ON DELETE CASCADE;
"""
)

EDGE_TABLE_DECLARATION_DDL_TEMPLATE = Template(
    """
{{name}}
      SOURCE KEY (id) REFERENCES {{partent}} (id)
      DESTINATION KEY ({{fkid}}) REFERENCES {{partent}} (id)
      LABEL {{name}}
"""
)


@dataclass
class EdgeMetaData:
    name: str
    parent: str
    fkid: str
    label: str


##########################################################################################
@dataclass
class InCounty:
    id: int
    county_id: int
    create_date: str

    def __init__(self, id, countylen):
        self.id = id
        self.county_id = fake.random_int(min=1, max=countylen)
        self.create_date = fake.date_time_between_dates(
            datetime_start=datetime.now() - relativedelta(years=3),
            datetime_end=datetime.now(),
        ).strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class CountyEdges:
    list_items: list[InCounty]
    metadata: EdgeMetaData

    def __init__(self, propertyList, countyList):
        self.list_items = [
            InCounty(i, len(countyList.list_items))
            for i in range(0, len(propertyList.list_items))
        ]
        self.metadata = EdgeMetaData(
            name="InCounty",
            parent="Property",
            fkid="property_id",
            label="IN_COUNTY",
        )


##########################################################################################
@dataclass
class HasOwner:
    id: int
    property_id: int
    create_date: str

    def __init__(self, id, propertylen):
        self.id = id
        self.property_id = fake.random_int(min=1, max=propertylen)
        self.create_date = fake.date_time_between_dates(
            datetime_start=datetime.now() - relativedelta(years=3),
            datetime_end=datetime.now(),
        ).strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class PropertyEdges:
    list_items: list[HasOwner]

    def __init__(self, propertyList, ownerList):
        self.list_items = [
            HasOwner(i, len(propertyList.list_items))
            for i in range(0, len(ownerList.list_items))
        ]
        self.metadata = EdgeMetaData(
            name="HasOwner",
            parent="Property",
            fkid="owner_id",
            label="HAS_OWNER",
        )


##########################################################################################
@dataclass
class HasCreditReport:
    id: int
    report_id: int
    create_date: str

    def __init__(self, id, ownerlen):
        self.id = id
        self.report_id = fake.random_int(min=1, max=ownerlen)
        self.create_date = fake.date_time_between_dates(
            datetime_start=datetime.now() - relativedelta(years=1),
            datetime_end=datetime.now(),
        ).strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class CreditEdges:
    list_items: list[HasCreditReport]

    def __init__(self, ownerList, creditList):
        self.list_items = [
            HasCreditReport(i, len(ownerList.list_items))
            for i in range(0, len(creditList.list_items))
        ]
        self.metadata = EdgeMetaData(
            name="HasCreditReport",
            parent="Owner",
            fkid="report_id",
            label="HAS_CREDIT_REPORT",
        )
