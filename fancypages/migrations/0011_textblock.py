# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0010_tabblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fancypages.ContentBlock')),
                ('text', models.TextField(default=b'Your text goes here.', verbose_name='Text')),
            ],
            options={
            },
            bases=('fancypages.contentblock',),
        ),
    ]
