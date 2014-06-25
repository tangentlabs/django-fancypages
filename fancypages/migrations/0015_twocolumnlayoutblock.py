# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0014_twitterblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwoColumnLayoutBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, to_field='id', serialize=False, to='fancypages.ContentBlock')),
                ('left_width', models.PositiveIntegerField(default=6, max_length=3, verbose_name='Left Width', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)])),
            ],
            options={
            },
            bases=('fancypages.contentblock',),
        ),
    ]
