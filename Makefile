.PHONY: dev sandbox

dev:
	pip install -r requirements.txt
	pip install -e .

sandbox: dev
	- rm sandbox/sandbox/db.sqlite3
	./sandbox/manage.py syncdb --noinput
	./sandbox/manage.py migrate
	- ./sandbox/manage.py loaddata sandbox/_fixtures/users.json
