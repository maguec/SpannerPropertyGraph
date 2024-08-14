#! /usr/bin/env python

from dataclasses import dataclass
from decimal import Decimal
from faker import Faker

fake = Faker()

credit_bureaus = ["CreditBureauA", "CreditBureauB", "CreditBureauC"]


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


##########################################################################################
@dataclass
class Property:
    id: int
    address: str
    bedrooms: int
    bathrooms: Decimal
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