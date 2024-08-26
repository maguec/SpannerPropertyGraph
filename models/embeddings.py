#! /usr/bin/env python

from dataclasses import dataclass
from decimal import Decimal
from faker import Faker
from jinja2 import Template
import os

from models.utils import typemap

fake = Faker()


AI_DDL_TEMPLATE = Template(
"""
CREATE MODEL EmbeddingsModel
INPUT(content STRING(MAX))
OUTPUT(
  embeddings
    STRUCT<
      statistics STRUCT<truncated BOOL, token_count FLOAT64>,
      values ARRAY<FLOAT64>>
)
REMOTE OPTIONS (
  endpoint = '//aiplatform.googleapis.com/projects/{{project}}/locations/us-central1/publishers/google/models/textembedding-gecko@003'
);
"""
)


##########################################################################################
@dataclass
class Embedding:
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
class Embeddings:
    list_items: list[Embedding]

    def __init__(self, items=10):
        self.list_items = [Embedding(id=i) for i in range(0, items)]

    def genddl(self):
        project = os.environ.get('gcp_project_id')
        if not project:
            print('the environment variable gcp_project_id not set')
            exit(1)
        tmpl = AI_DDL_TEMPLATE.render(project=project)
        return tmpl

