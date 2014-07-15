# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from configurations import values

import fancypages as fp

from . import common


class StandaloneFancypages(common.Common):
    SANDBOX_MODULE = 'standalone_fancypages'

    @property
    def INSTALLED_APPS(self):
        return self.REQUIRED_APPS + fp.get_fancypages_apps()


class StandaloneFancypagesPostgres(StandaloneFancypages):
    POSTGRES_PORT = values.Value(5432)

    @property
    def DATABASES(self):
        return {'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'fp_sandbox',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': self.POSTGRES_PORT}}


class StandaloneFancypagesMysql(StandaloneFancypages):
    MYSQL_PORT = values.Value(3306)

    @property
    def DATABASES(self):
        return {'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'fp_sandbox',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': 3306}}
