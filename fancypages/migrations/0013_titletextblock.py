# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0012_threecolumnlayoutblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='TitleTextBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fancypages.ContentBlock')),
                ('title', models.CharField(default=b'Your title goes here.', max_length=100, verbose_name='Title')),
                ('text', models.TextField(default=b'Your text goes here.', verbose_name='Text')),
            ],
            options={
            },
            bases=('fancypages.contentblock',),
        ),
    ]
