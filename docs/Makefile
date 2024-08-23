default: help

##@ Utility
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

gendiagrams: ## Generate Schema
	@echo "Generating Diagrams"
	@rm -f *.png
	@dot -Tpng datasources.dot > datasources.png
	@dot -Tpng graph.dot > graph.png
