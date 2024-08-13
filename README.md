# Graph Example of Property Queries

## Create the Spanner Instance

```bash

gcloud spanner instances create properties --description="Property Graph Database" --nodes=1 --config=regional-us-west1

```

## Create the database with the necessary DDL

```bash

gcloud spanner databases create propertydb --instance  properties --ddl-file=PropertyGraphDDL.sql

```

