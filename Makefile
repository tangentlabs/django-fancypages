.PHONY: compile-static

STATIC_DIR="fancypages/static/fancypages/"

smaller:
	uglifyjs fancypages/static/fancypages/libs/wysihtml5/wysihtml5-config.js > fancypages/static/fancypages/libs/wysihtml5/wysihtml5-config.min.js
	uglifyjs fancypages/static/fancypages/libs/wysihtml5/wysihtml5-0.3.0.js > fancypages/static/fancypages/libs/wysihtml5/wysihtml5-0.3.0.min.js

dev:
	pip install -e .
	pip install -r requirements.txt

compile-static:
	- mkdir -p fancypages/css
	lessc ${STATIC_DIR}less/page-management.less > ${STATIC_DIR}css/page-management.css
	lessc ${STATIC_DIR}less/fancypages.less > ${STATIC_DIR}css/fancypages.css
	lessc ${STATIC_DIR}less/assets.less > ${STATIC_DIR}css/assets.css
	lessc ${STATIC_DIR}less/page.less > ${STATIC_DIR}css/page.css
