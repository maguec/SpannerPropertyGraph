#! /usr/bin/env python

from models.nodes import *
from models.edges import *
from models.utils import *
from models.embeddings import *
from google.cloud import spanner

if __name__ == "__main__":
    s = spanner.Client()
    instance = s.instance("properties")
    client = instance.database("propertydb")
    owners = Owners(items=550)
    client.run_in_transaction(writeSpanner,owners)
    counties = Counties(items=60)
    client.run_in_transaction(writeSpanner,counties)
    properties = Properties(items=1000)
    client.run_in_transaction(writeSpanner, properties)
    embeddings = Embeddings(items=len(properties.list_items))
    client.run_in_transaction(writeSpanner, embeddings)
    credit_reports = CreditReports(items=len(owners.list_items))
    client.run_in_transaction(writeSpanner, credit_reports)
    in_county = CountyEdges(properties, counties)
    client.run_in_transaction(writeSpanner, in_county)
    has_owner = PropertyEdges(properties, owners)
    client.run_in_transaction(writeSpanner, has_owner)
    has_credit = CreditEdges(owners, credit_reports)
    client.run_in_transaction(writeSpanner, has_credit)
    social = SocialEdges(owners)
    client.run_in_transaction(writeSpanner, social)
    embedding_edges = EmbeddingEdges(properties)
    client.run_in_transaction(writeSpanner, embedding_edges)
    
