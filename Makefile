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
