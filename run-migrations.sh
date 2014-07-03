#! /bin/bash

DJANGO_VERSION=`./sandboxes/fancypages/manage.py --version`
DJANGO_MINOR=${DJANGO_VERSION:2:1}
SANDBOX=${SANDBOX:-fancypages}

if [ ${DJANGO_MINOR} -lt 7 ];
then
    echo "Running South migrations";
    python sandboxes/${SANDBOX}/manage.py syncdb --noinput
    python sandboxes/${SANDBOX}/manage.py migrate
else
    echo "Running Django migrations";
    python sandboxes/${SANDBOX}/manage.py migrate --noinput
fi
