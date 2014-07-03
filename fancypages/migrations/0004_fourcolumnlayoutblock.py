# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0003_carouselblock_fancypage'),
    ]

    operations = [
        migrations.CreateModel(
            name='FourColumnLayoutBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, to_field='id', serialize=False, to='fancypages.ContentBlock')),
            ],
            options={
            },
            bases=('fancypages.contentblock',),
        ),
    ]
