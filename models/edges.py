#! /usr/bin/env python

from dataclasses import dataclass
from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker

fake = Faker()

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

    def __init__(self, propertyList, countyList):
        self.list_items = [InCounty(i, len(countyList.list_items)) for i in range(0, len(propertyList.list_items))]

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
        self.list_items = [HasOwner(i, len(propertyList.list_items)) for i in range(0, len(ownerList.list_items))]

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
        self.list_items = [HasCreditReport(i, len(ownerList.list_items)) for i in range(0, len(creditList.list_items))]
