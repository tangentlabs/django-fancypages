.PHONY: compile-static test

STATIC_DIR="fancypages/static/fancypages/"


compile-static:
	- mkdir -p fancypages/css
	lessc ${STATIC_DIR}less/page-management.less > ${STATIC_DIR}css/page-management.css
	lessc ${STATIC_DIR}less/fancypages.less > ${STATIC_DIR}css/fancypages.css
	lessc ${STATIC_DIR}less/assets.less > ${STATIC_DIR}css/assets.css
	lessc ${STATIC_DIR}less/page.less > ${STATIC_DIR}css/page.css

test: test-fancypages test-oscar-fancypages test-migration-sqlite

travis:
	${MAKE} test-fancypages
	pip install -r requirements_oscar.txt
	${MAKE} test-oscar-fancypages

test-fancypages:
	py.test --pep8
	py.test -m integration

test-oscar-fancypages:
	USE_OSCAR_SANDBOX=true py.test --pep8 --cov fancypages
	USE_OSCAR_SANDBOX=true py.test -m integration

test-migration-sqlite:
	- rm sandboxes/oscar_fancypages/sandbox/migration_test.sqlite
	./sandboxes/oscar_fancypages/manage.py syncdb --noinput --migrate --settings=sandbox.settings_migration_sqlite
