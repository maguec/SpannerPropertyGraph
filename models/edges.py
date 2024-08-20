#! /usr/bin/env python

from dataclasses import dataclass
from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker
from jinja2 import Template
from models.utils import typemap

fake = Faker()

EDGE_TABLE_DDL_TEMPLATE = Template(
    """
CREATE TABLE {{name}} (
    {% for field in fields -%}
    {{field}},
    {% endfor -%}
  FOREIGN KEY ({{fkid}}) REFERENCES {{parent}} (id)
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
    property_id: int
    create_date: str

    def __init__(self, id, countylen, propertylen):
        self.id = id
        self.county_id = fake.random_int(min=1, max=countylen)
        self.property_id = fake.random_int(min=1, max=propertylen)
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
            InCounty(i, len(countyList.list_items), len(propertyList.list_items))
            for i in range(0, len(propertyList.list_items))
        ]
        self.metadata = EdgeMetaData(
            name="InCounty",
            parent="Property",
            fkid="property_id",
            label="IN_COUNTY",
        )

    def genddl(self):
        c = InCounty(id=-1, countylen=1, propertylen=1)
        name = c.__class__.__name__
        fields = []
        for field in InCounty.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = EDGE_TABLE_DDL_TEMPLATE.render(
            name=name, fields=fields, parent=self.metadata.parent,fkid=self.metadata.fkid
        )
        return tmpl

    def gendeclarationddl(self):
        c = InCounty(id=-1, countylen=1, propertylen=1)
        name = c.__class__.__name__
        fields = []
        for field in InCounty.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = EDGE_TABLE_DECLARATION_DDL_TEMPLATE.render(
            name=name, fields=fields, partent=self.metadata.parent,fkid=self.metadata.fkid
        )
        return tmpl


##########################################################################################
@dataclass
class HasOwner:
    id: int
    property_id: int
    owner_id: int
    create_date: str

    def __init__(self, id, propertylen, ownerlen):
        self.id = id
        self.owner_id = fake.random_int(min=1, max=ownerlen)
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
            HasOwner(i, len(propertyList.list_items), len(ownerList.list_items))
            for i in range(0, len(ownerList.list_items))
        ]
        self.metadata = EdgeMetaData(
            name="HasOwner",
            parent="Property",
            fkid="owner_id",
            label="HAS_OWNER",
        )

    def genddl(self):
        c = HasOwner(id=-1, propertylen=1, ownerlen=1)
        name = c.__class__.__name__
        fields = []
        for field in HasOwner.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = EDGE_TABLE_DDL_TEMPLATE.render(
            name=name, fields=fields, parent=self.metadata.parent,fkid=self.metadata.fkid
        )
        return tmpl
    def gendeclarationddl(self):
        c = HasOwner(id=-1, propertylen=1, ownerlen=1)
        name = c.__class__.__name__
        fields = []
        for field in HasOwner.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = EDGE_TABLE_DECLARATION_DDL_TEMPLATE.render(
            name=name, fields=fields, partent=self.metadata.parent,fkid=self.metadata.fkid
        )
        return tmpl


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

    def genddl(self):
        c = HasCreditReport(id=-1, ownerlen=1)
        name = c.__class__.__name__
        fields = []
        for field in HasCreditReport.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = EDGE_TABLE_DDL_TEMPLATE.render(
            name=name, fields=fields, parent=self.metadata.parent,fkid=self.metadata.fkid
        )
        return tmpl
    def gendeclarationddl(self):
        c = HasCreditReport(id=-1, ownerlen=1)
        name = c.__class__.__name__
        fields = []
        for field in HasCreditReport.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = EDGE_TABLE_DECLARATION_DDL_TEMPLATE.render(
            name=name, fields=fields, partent=self.metadata.parent,fkid=self.metadata.fkid
        )
        return tmpl
