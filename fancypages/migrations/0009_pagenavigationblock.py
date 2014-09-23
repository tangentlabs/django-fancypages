# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0008_orderedcontainer'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageNavigationBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fancypages.ContentBlock')),
                ('depth', models.PositiveIntegerField(default=2, verbose_name='Navigation depth')),
                ('is_relative', models.BooleanField(default=False, verbose_name='Is navigation relative to this page?')),
            ],
            options={
            },
            bases=('fancypages.contentblock',),
        ),
    ]
