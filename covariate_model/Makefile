

remote:
	scp -i ~/.ssh/id_rsa.pub covariates.sql sumotools1.webapp.phx1.mozilla.com:~/hb-covariates
	echo "now ssh to sumotools, and run it on 'ir', yes this sucks."
	echo "on sumotools1: cd hb-covariates; mysql --login-path=input --batch -D input_mozilla_org_new < covariates.sql > hb-data.tsv"

hb:
	scp -i ~/.ssh/id_rsa.pub sumotools1.webapp.phx1.mozilla.com:~/hb-covariates/hb-data.tsv .


surveys:
	curl "http://app.surveygizmo.com/reportsview/?key=28049-5305096-77ff479273501cbf114a9d7b6ba25431&print=true" > pb-data.csv


reformat:
	python reformat.py pb-data.csv hb-data.tsv > hb-with-covariates.csv

clean:
	rm -f hb-data.tsv pb-data.csv hb-with-covariates.csv


build: clean surveys hb reformat

