# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0007_imageblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedContainer',
            fields=[
                ('container_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fancypages.Container')),
                ('display_order', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=('fancypages.container',),
        ),
    ]
