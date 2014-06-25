# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0015_twocolumnlayoutblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, to_field='id', serialize=False, to='fancypages.ContentBlock')),
                ('source', models.CharField(max_length=50, verbose_name='Video Type', choices=[(b'youtube', 'YouTube video')])),
                ('video_code', models.CharField(max_length=50, verbose_name='Video Code')),
            ],
            options={
            },
            bases=('fancypages.contentblock',),
        ),
    ]
