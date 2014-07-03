.PHONY: compile-static tests docs

STATIC_DIR="fancypages/static/fancypages/"
ifndef PYTEST_OPTS
    PYTEST_OPTS=--pep8 tests
endif
ifndef DJANGO_POSTGRES_PORT
    DJANGO_POSTGRES_PORT=5432
endif
ifndef DJANGO_MYSQL_PORT
    DJANGO_MYSQL_PORT=3306
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
	- psql -h localhost -p ${DJANGO_POSTGRES_PORT} -U postgres -c "DROP DATABASE fp_sandbox;"
	psql -h localhost -p ${DJANGO_POSTGRES_PORT} -U postgres -c "CREATE DATABASE fp_sandbox;"
	DJANGO_CONFIGURATION="FancypagesPostgres" SANDBOX="fancypages" ./run-migrations.sh

test-mysql:
	-  mysql -h 127.0.0.1 -P ${DJANGO_MYSQL_PORT} -u root -e 'DROP DATABASE fp_sandbox;'
	mysql -h 127.0.0.1 -P ${DJANGO_MYSQL_PORT} -u root -e 'CREATE DATABASE fp_sandbox;'
	DJANGO_CONFIGURATION="FancypagesMysql" SANDBOX="fancypages" ./run-migrations.sh

test-ofp-postgres:
	- psql -h localhost -p ${DJANGO_POSTGRES_PORT} -U postgres -c "DROP DATABASE ofp_sandbox;"
	psql -h localhost -p ${DJANGO_POSTGRES_PORT} -U postgres -c "CREATE DATABASE ofp_sandbox;"
	DJANGO_CONFIGURATION="OscarFancypagesPostgres" SANDBOX="oscar_fancypages" ./run-migrations.sh

test-ofp-mysql:
	-  mysql -h 127.0.0.1 -P ${DJANGO_MYSQL_PORT} -u root -e 'DROP DATABASE ofp_sandbox;'
	mysql -h 127.0.0.1 -P ${DJANGO_MYSQL_PORT} -u root -e 'CREATE DATABASE ofp_sandbox;'
	DJANGO_CONFIGURATION="OscarFancypagesMysql" SANDBOX="oscar_fancypages" ./run-migrations.sh

docs:
	${MAKE} -C docs html
