default: help

##@ Utility
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

genschema: ## Generate Schema
	@echo "Generating Schema"
	@rm -f PropertyGraphDDL.sql
	@python3 ./generate_ddl.py > PropertyGraphDDL.sql


loadschema: ## Load Schema onto Spanner
	@echo "Loading Schema"
	@gcloud spanner databases create propertydb --instance  properties --ddl-file=PropertyGraphDDL.sql

clean: ## Remove all generated files
	@rm -f *.csv
	@find . -name \*.pyc -delete
	@find . -name __pycache__ -delete

dbclean: ## Remove all  table dat
	@gcloud spanner databases execute-sql propertydb  --instance=properties --sql='DELETE from Owner WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=properties --sql='DELETE from Property WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=properties --sql='DELETE from CreditReport WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=properties --sql='DELETE from County WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=properties --sql='DELETE from InCounty WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=properties --sql='DELETE from HasCreditReport WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=properties --sql='DELETE from HasOwner WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=properties --sql='DELETE from HasSocial WHERE id < 100000000;'

dbdrop: ## Drop all tables DANGER
	@gcloud spanner databases  delete  propertydb --instance properties


instancecreate: ## Spin up a single node Spanner instance
	@gcloud spanner instances create properties --description="Property Graph Database" --nodes=1 --config=regional-us-west1


instancedelete: ## Shutdown the Spanner instance
	@gcloud spanner instances delete properties

