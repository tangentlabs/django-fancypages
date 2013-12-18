.PHONY: compile-static test

STATIC_DIR="fancypages/static/fancypages/"


compile-static:
	- mkdir -p fancypages/css
	lessc ${STATIC_DIR}less/page-management.less > ${STATIC_DIR}css/page-management.css
	lessc ${STATIC_DIR}less/fancypages.less > ${STATIC_DIR}css/fancypages.css
	lessc ${STATIC_DIR}less/assets.less > ${STATIC_DIR}css/assets.css
	lessc ${STATIC_DIR}less/page.less > ${STATIC_DIR}css/page.css

test:
	py.test --pep8
	USE_OSCAR_SANDBOX=true py.test --pep8 --cov fancypages
	py.test -m integration
	USE_OSCAR_SANDBOX=true py.test -m integration
