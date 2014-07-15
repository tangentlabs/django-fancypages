#! /bin/bash

DJANGO_VERSION=`./sandbox/manage.py --version`
DJANGO_MINOR=${DJANGO_VERSION:2:1}

if [ ${DJANGO_MINOR} -lt 7 ];
then
    echo "Running South migrations";
    python sandbox/manage.py syncdb --noinput
    python sandbox/manage.py migrate
else
    echo "Running Django migrations";
    python sandbox/manage.py migrate --noinput
fi
