.PHONY: dev sandbox

smaller:
	uglifyjs fancypages/static/fancypages/libs/wysihtml5/wysihtml5-config.js > fancypages/static/fancypages/libs/wysihtml5/wysihtml5-config.min.js
	uglifyjs fancypages/static/fancypages/libs/wysihtml5/wysihtml5-0.3.0.js > fancypages/static/fancypages/libs/wysihtml5/wysihtml5-0.3.0.min.js

dev:
	pip install -e .
	pip install -r requirements.txt

sandbox: dev
	- rm sandbox/sandbox/db.sqlite3
	./sandbox/manage.py syncdb --noinput
	./sandbox/manage.py migrate
	- ./sandbox/manage.py loaddata sandbox/_fixtures/users.json
