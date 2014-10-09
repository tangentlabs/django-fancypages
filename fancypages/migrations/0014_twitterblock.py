# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0013_titletextblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fancypages.ContentBlock')),
                ('username', models.CharField(max_length=50, verbose_name='Twitter username')),
                ('max_tweets', models.PositiveIntegerField(default=5, verbose_name='Maximum tweets')),
            ],
            options={
            },
            bases=('fancypages.contentblock',),
        ),
    ]
