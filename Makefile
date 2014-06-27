.PHONY: compile-static tests

STATIC_DIR="fancypages/static/fancypages/"
ifndef PYTEST_OPTS
    PYTEST_OPTS=--pep8 tests
endif

dev:
	pip install -e .
	pip install -r requirements_dev.txt

compile-static:
	grunt

tests: test-fancypages test-oscar-fancypages

test-fancypages:
	@echo "Running Test"
	py.test ${PYTEST_OPTS}
	@echo "Running PostgreSQL migrations"
	${MAKE} test-postgres
	@echo "Running MySQL migrations"
	${MAKE} test-mysql

test-oscar-fancypages:
	pip install -r requirements_oscar.txt
	DJANGO_CONFIGURATION='OscarTest' py.test ${PYTEST_OPTS}
	${MAKE} test-ofp-postgres
	${MAKE} test-ofp-mysql

test-postgres:
	- psql -h localhost -p 5432 -U postgres -c "DROP DATABASE fp_sandbox;"
	psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE fp_sandbox;"
	DJANGO_CONFIGURATION="FancypagesPostgres" SANDBOX="fancypages" ./run-migrations.sh

test-mysql:
	-  mysql -h 127.0.0.1 -P 3306 -u root -e 'DROP DATABASE fp_sandbox;'
	mysql -h 127.0.0.1 -P 3306 -u root -e 'CREATE DATABASE fp_sandbox;'
	DJANGO_CONFIGURATION="FancypagesMysql" SANDBOX="fancypages" ./run-migrations.sh

test-ofp-postgres:
	- psql -h localhost -p 5432 -U postgres -c "DROP DATABASE ofp_sandbox;"
	psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE ofp_sandbox;"
	DJANGO_CONFIGURATION="OscarFancypagesPostgres" SANDBOX="oscar_fancypages" ./run-migrations.sh

test-ofp-mysql:
	-  mysql -h 127.0.0.1 -P 3306 -u root -e 'DROP DATABASE ofp_sandbox;'
	mysql -h 127.0.0.1 -P 3306 -u root -e 'CREATE DATABASE ofp_sandbox;'
	DJANGO_CONFIGURATION="OscarFancypagesMysql" SANDBOX="oscar_fancypages" ./run-migrations.sh

docs:
	${MAKE} -C docs html
