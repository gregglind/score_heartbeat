
build: remote sg-data.csv hb-data-us1.tsv firefox.json reformat

remote:
	scp -i ~/.ssh/id_rsa.pub covariates.sql sumotools1.webapp.phx1.mozilla.com:~/hb-covariates
	#@echo "now ssh to sumotools, and run it on 'ir', yes this sucks."
	#@echo "on sumotools1: "
	#@echo "cd ~/hb-covariates; mysql --login-path=input --batch -D input_mozilla_org_new < covariates.sql > hb-data-us1.tsv"
	ssh sumotools1.webapp.phx1.mozilla.com -i ~/.ssh/id_rsa.pub "cd ~/hb-covariates; rm -f hb-data-us1.tsv.gz; mysql --login-path=input --batch -D input_mozilla_org_new < covariates.sql > hb-data-us1.tsv; gzip -f hb-data-us1.tsv"

firefox.json:
	curl "https://product-details.mozilla.org/firefox.json" > firefox.json

# hb-data
hb-data-us1.tsv:
	scp -i ~/.ssh/id_rsa.pub sumotools1.webapp.phx1.mozilla.com:~/hb-covariates/hb-data-us1.tsv.gz .
	gunzip hb-data-us1.tsv.gz


# surveys
sg-data.csv:
	curl "http://app.surveygizmo.com/reportsview/?key=28049-5441187-88cd6ce8aab9961a4147d8b0dc50ae38&print=true" > sg-data.csv

reformat:
	python reformat.py sg-data.csv hb-data-us1.tsv firefox.json > us1-with-covariates.csv

.PHONY: clean
clean:
	rm -f hb-data-us1.tsv sg-data.csv hb-with-covariates.csv firefox.json



