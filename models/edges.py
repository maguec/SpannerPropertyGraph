#! /usr/bin/env python

from dataclasses import dataclass
from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker
from jinja2 import Template
from models.utils import typemap, oneToManyGen

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
      SOURCE KEY ({{ source }}) REFERENCES {{parent}} (id)
      DESTINATION KEY ({{fkid}}) REFERENCES {{target}} (id)
      LABEL {{label}}
"""
)


@dataclass
class EdgeMetaData:
    name: str
    parent: str
    fkid: str
    label: str
    target: str
    source: str


##########################################################################################
@dataclass
class InCounty:
    id: int
    county_id: int
    property_id: int
    create_date: str

    def __init__(self, id, countylen, propertylen):
        self.id = id
        self.county_id = fake.random_int(min=0, max=countylen - 1)
        self.property_id = fake.random_int(min=0, max=propertylen - 1)
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
            source="id",
            target="County"
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
            name=name,
            fields=fields,
            parent=self.metadata.parent,
            fkid=self.metadata.fkid,
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
            name=name,
            fields=fields,
            parent=self.metadata.parent,
            fkid=self.metadata.fkid,
            label=self.metadata.label,
            source=self.metadata.source,
            target=self.metadata.target,
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
        self.owner_id = fake.random_int(min=0, max=ownerlen - 1)
        self.property_id = fake.random_int(min=0, max=propertylen - 1)
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
            source="id",
            target="Owner",
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
            name=name,
            fields=fields,
            parent=self.metadata.parent,
            fkid=self.metadata.fkid,
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
            name=name,
            fields=fields,
            parent=self.metadata.parent,
            fkid=self.metadata.fkid,
            label=self.metadata.label,
            source=self.metadata.source,
            target=self.metadata.target,
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
        self.report_id = fake.random_int(min=0, max=ownerlen - 1)
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
            source="id",
            target="CreditReport"
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
            name=name,
            fields=fields,
            parent=self.metadata.parent,
            fkid=self.metadata.fkid,
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
            name=name,
            fields=fields,
            parent=self.metadata.parent,
            fkid=self.metadata.fkid,
            label=self.metadata.label,
            source=self.metadata.source,
            target=self.metadata.target,
        )
        return tmpl
##########################################################################################
# Social Graph
@dataclass
class HasSocial:
    id: int
    dest_owner: int
    since: str

    def __init__(self, id, dest):
        self.id = id
        self.dest_owner = dest
        self.since = fake.date_time_between_dates(
            datetime_start=datetime.now() - relativedelta(years=15),
            datetime_end=datetime.now(),
        ).strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class SocialEdges:
    list_items: list[HasSocial]

    def __init__(self, ownerList):
        items = oneToManyGen(len(ownerList.list_items), len(ownerList.list_items), 9)
        self.list_items = [
            HasSocial(items[i][0], items[i][1])
            for i in range(0, len(items)-1)
        ]
        self.metadata = EdgeMetaData(
            name="HasSocialConnections",
            parent="Owner",
            fkid="dest_owner",
            label="KNOWS",
            source = "id",
            target="Owner",
        )

    def genddl(self):
        c = HasSocial(1, 2)
        name = c.__class__.__name__
        fields = []
        for field in HasSocial.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = EDGE_TABLE_DDL_TEMPLATE.render(
            name=name,
            fields=fields,
            parent=self.metadata.parent,
            fkid=self.metadata.fkid,
        )
        return tmpl

    def gendeclarationddl(self):
        c = HasSocial(1, 2)
        name = c.__class__.__name__
        fields = []
        for field in HasSocial.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = EDGE_TABLE_DECLARATION_DDL_TEMPLATE.render(
            name=name,
            fields=fields,
            parent=self.metadata.parent,
            fkid=self.metadata.fkid,
            label=self.metadata.label,
            source=self.metadata.source,
            target=self.metadata.target,
        )
        return tmpl
