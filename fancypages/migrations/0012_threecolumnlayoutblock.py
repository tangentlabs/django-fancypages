# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0011_textblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreeColumnLayoutBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fancypages.ContentBlock')),
            ],
            options={
            },
            bases=('fancypages.contentblock',),
        ),
    ]
