.PHONY: compile-static tests

STATIC_DIR="fancypages/static/fancypages/"
ifndef PYTEST_OPTS
    PYTEST_OPTS="--pep8"
endif

smaller:
	uglifyjs fancypages/static/fancypages/libs/wysihtml5/wysihtml5-config.js > fancypages/static/fancypages/libs/wysihtml5/wysihtml5-config.min.js
	uglifyjs fancypages/static/fancypages/libs/wysihtml5/wysihtml5-0.3.0.js > fancypages/static/fancypages/libs/wysihtml5/wysihtml5-0.3.0.min.js

dev:
	pip install -e .
	pip install -r requirements.txt

compile-static:
	grunt

tests: test-fancypages test-oscar-fancypages

test-fancypages:
	py.test ${PYTEST_OPTS}

test-oscar-fancypages:
	pip install -r requirements_oscar.txt
	DJANGO_CONFIGURATION='OscarTest' py.test  ${PYTEST_OPTS}

test-migrations: test-postgres test-mysql

test-postgres:
	- psql -h localhost -p 5432 -U postgres -c "DROP DATABASE fp_sandbox;"
	psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE fp_sandbox;"
	DJANGO_CONFIGURATION="FancypagesPostgres" ./sandboxes/fancypages/manage.py migrate --noinput

test-mysql:
	-  mysql -h 127.0.0.1 -P 3306 -u root -e 'DROP DATABASE fp_sandbox;'
	mysql -h 127.0.0.1 -P 3306 -u root -e 'CREATE DATABASE fp_sandbox;'
	DJANGO_CONFIGURATION="FancypagesMysql" ./sandboxes/fancypages/manage.py migrate --noinput

docs:
	${MAKE} -C docs html
