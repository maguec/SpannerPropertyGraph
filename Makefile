GOOGLE_CLOUD_REGION ?= $(GOOGLE_CLOUD_REGION)
GOOGLE_CLOUD_SPANNER_INSTANCE ?= $(GOOGLE_CLOUD_SPANNER_INSTANCE)

default: help

# A target to specifically check for uv
check_uv:
	@command -v uv >/dev/null 2>&1 || (echo "🚨 ERROR: 'uv' not found. Please install it." && exit 1)
	@echo "✅ uv is installed and ready."

check_env:
ifeq ($(strip $(gcp_project_id)),)
    # The $(error ...) function prints the message and immediately stops the build.
    (echo "🚨 ERROR: 'ENV var gcp_project_id' not set. Please set it." && exit 1)
endif

##@ Utility
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

genschema: check_env check_uv ## Generate Schema
	@echo "Generating Schema"
	@rm -f RealEstateGraphDDL.sql
	@uv run generate_ddl.py > RealEstateGraphDDL.sql

loaddata: check_env check_uv ## Load data into the database
	@echo "Loading Data"
	@uv run generate_data.py

loadschema: ## Load Schema onto Spanner
	@echo "Loading Schema"
	@gcloud spanner databases create propertydb --instance  $(GOOGLE_CLOUD_SPANNER_INSTANCE) --ddl-file=RealEstateGraphDDL.sql

clean: ## Remove all generated files
	@rm -f *.csv
	@find . -name \*.pyc -delete
	@find . -name __pycache__ -delete

dbclean: ## Remove all  table dat
	@gcloud spanner databases execute-sql propertydb  --instance=$(GOOGLE_CLOUD_SPANNER_INSTANCE) --sql='DELETE from Owner WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=$(GOOGLE_CLOUD_SPANNER_INSTANCE) --sql='DELETE from Property WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=$(GOOGLE_CLOUD_SPANNER_INSTANCE) --sql='DELETE from CreditReport WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=$(GOOGLE_CLOUD_SPANNER_INSTANCE) --sql='DELETE from County WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=$(GOOGLE_CLOUD_SPANNER_INSTANCE) --sql='DELETE from Company WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=$(GOOGLE_CLOUD_SPANNER_INSTANCE) --sql='DELETE from InCounty WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=$(GOOGLE_CLOUD_SPANNER_INSTANCE) --sql='DELETE from HasCreditReport WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=$(GOOGLE_CLOUD_SPANNER_INSTANCE) --sql='DELETE from HasOwner WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=$(GOOGLE_CLOUD_SPANNER_INSTANCE) --sql='DELETE from HasSocial WHERE id < 100000000;'
	@gcloud spanner databases execute-sql propertydb  --instance=$(GOOGLE_CLOUD_SPANNER_INSTANCE) --sql='DELETE from HasCompany WHERE id < 100000000;'

dbdrop: ## Drop all tables DANGER
	@gcloud spanner databases  delete  propertydb --instance $(GOOGLE_CLOUD_SPANNER_INSTANCE)


instancecreate: ## Spin up a single node Spanner instance
	@gcloud spanner instances create $(GOOGLE_CLOUD_SPANNER_INSTANCE) --description="Property Graph Database" --config=regional-$(GOOGLE_CLOUD_REGION) --edition=ENTERPRISE  --processing-units=100 --default-backup-schedule-type=NONE


instancedelete: ## Shutdown the Spanner instance
	@gcloud spanner instances delete $(GOOGLE_CLOUD_SPANNER_INSTANCE)

