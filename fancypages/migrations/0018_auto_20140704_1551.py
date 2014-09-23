# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0017_auto_20140630_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fancypages.ContentBlock')),
                ('form_selection', models.CharField(max_length=255, verbose_name='form selection', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('fancypages.contentblock',),
        ),
    ]
