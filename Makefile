.PHONY: dev sandbox

dev:
	pip install -e .
	pip install -r requirements.txt

sandbox: dev
	- rm sandbox/sandbox/sandbox.sqlite3
	./sandbox/manage.py syncdb --noinput
	./sandbox/manage.py migrate
