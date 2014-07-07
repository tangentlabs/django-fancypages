# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0018_auto_20140704_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formblock',
            name='form_selection',
            field=models.CharField(blank=True, max_length=255, verbose_name='form selection'),
        ),
    ]
