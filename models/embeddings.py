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
CREATE MODEL EmbedsModel
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
class Embed:
    id: int
    embedding: list[float]

    def __init__(self, id):
        self.id = id
        self.embedding = [fake.pyfloat(min_value=-1.0, max_value=1.0) for _ in range(768)]


@dataclass
class Embeds:
    list_items: list[Embed]

    def __init__(self, items=10):
        self.list_items = [Embed(id=i) for i in range(0, items)]

    def genaiddl(self):
        project = os.environ.get('gcp_project_id')
        if not project:
            print('the environment variable gcp_project_id not set')
            exit(1)
        tmpl = AI_DDL_TEMPLATE.render(project=project)
        return tmpl

    def genddl(self):
        c = Embed(id=-1)
        name = c.__class__.__name__
        fields = []
        for field in Embed.__dataclass_fields__:
            fields.append(
                "  {}\t\t{}".format(field, typemap(type(getattr(c, field)).__name__))
            )
        tmpl = NODE_DDL_TEMPLATE.render(name=name, fields=fields)
        return tmpl
