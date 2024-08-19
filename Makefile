default: genschema


genschema:
	@echo "Generating Schema"
	@rm -f PropertyGraphDDL.sql
	@python3 ./generate_ddl.py > PropertyGraphDDL.sql


loadschema:
	@echo "Loading Schema"
	@gcloud spanner databases create propertydb --instance  properties --ddl-file=PropertyGraphDDL.sql

clean:
	@rm *.csv
