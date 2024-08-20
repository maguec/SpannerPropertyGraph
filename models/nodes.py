#! /usr/bin/env python

from dataclasses import dataclass
from decimal import Decimal
from faker import Faker
from jinja2 import Template

from models.utils import typemap

fake = Faker()

credit_bureaus = ["CreditBureauA", "CreditBureauB", "CreditBureauC"]

NODE_DDL_TEMPLATE = Template(
    """CREATE TABLE {{name}} (
    {% for field in fields -%}
    {{field}},
    {% endfor -%}
    ) PRIMARY KEY (id);
"""
)


##########################################################################################
@dataclass
class County:
    id: int
    name: str
    tax_rate: Decimal
    postcode: str

    def __init__(self, id):
        self.id = id
        self.name = fake.city()
        self.tax_rate = (
            fake.pydecimal(left_digits=0, right_digits=3, positive=True) * 10
        )
        self.postcode = fake.postcode()


@dataclass
class Counties:
    list_items: list[County]

    def __init__(self, items=10):
        self.list_items = [County(id=i) for i in range(0, items)]

    def writeSpanner(self, transaction, batch=10):
        rows = []
        columns = County.__dataclass_fields__.keys()
        for item in self.list_items:
            #rows.append((item.id, item.name, item.tax_rate, item.postcode))
            rows.append(tuple(item.__dict__.values()))
            if len(rows) % batch == 0:
                transaction.insert(table="County", columns=columns, values=rows)
                print("wrote {} rows".format(len(rows)))
                rows = []
        if len(rows) > 0:
            transaction.insert(table="County", columns=columns, values=rows)

    def genddl(self):
        c = County(id=-1)
        name = c.__class__.__name__
        fields = []
        for field in County.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = NODE_DDL_TEMPLATE.render(name=name, fields=fields)
        return tmpl


##########################################################################################
@dataclass
class Property:
    id: int
    address: str
    bedrooms: int
    bathrooms: int
    price: int

    def __init__(self, id):
        self.id = id
        self.address = fake.address().split("\n")[0]
        self.bedrooms = fake.random_int(min=1, max=8)
        self.bathrooms = fake.random_int(min=1, max=5)
        self.price = fake.random_int(min=300000, max=2000000)


@dataclass
class Properties:
    list_items: list[Property]

    def __init__(self, items=10):
        self.list_items = [Property(id=i) for i in range(0, items)]

    def genddl(self):
        c = Property(id=-1)
        name = c.__class__.__name__
        fields = []
        for field in Property.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = NODE_DDL_TEMPLATE.render(name=name, fields=fields)
        return tmpl


##########################################################################################
@dataclass
class Owner:
    id: int
    name: str
    ssn: str

    def __init__(self, id):
        self.id = id
        self.name = fake.name()
        self.ssn = fake.ssn()


@dataclass
class Owners:
    list_items: list[Owner]

    def __init__(self, items=10):
        self.list_items = [Owner(id=i) for i in range(0, items)]

    def genddl(self):
        c = Owner(id=-1)
        name = c.__class__.__name__
        fields = []
        for field in Owner.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = NODE_DDL_TEMPLATE.render(name=name, fields=fields)
        return tmpl


##########################################################################################
@dataclass
class CreditReport:
    id: int
    score: int
    bureau: str

    def __init__(self, id):
        self.id = id
        self.score = fake.random_int(min=300, max=850)
        self.bureau = fake.random_element(elements=credit_bureaus)


@dataclass
class CreditReports:
    list_items: list[CreditReport]

    def __init__(self, items=10):
        self.list_items = [CreditReport(id=i) for i in range(0, items)]

    def genddl(self):
        c = CreditReport(id=-1)
        name = c.__class__.__name__
        fields = []
        for field in CreditReport.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = NODE_DDL_TEMPLATE.render(name=name, fields=fields)
        return tmpl
