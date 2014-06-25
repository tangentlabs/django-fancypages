# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import fancypages.assets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '__first__'),
        ('fancypages', '0005_horizontalseparatorblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAndTextBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, to_field='id', serialize=False, to='fancypages.ContentBlock')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Image title', blank=True)),
                ('alt_text', models.CharField(max_length=100, null=True, verbose_name='Alternative text', blank=True)),
                ('link', models.CharField(max_length=500, null=True, verbose_name='Link URL', blank=True)),
                ('image_asset', fancypages.assets.fields.AssetKey(verbose_name='Image asset', to_field='id', blank=True, to='assets.ImageAsset', null=True)),
                ('text', models.TextField(default='Your text goes here.', verbose_name='Text')),
            ],
            options={
            },
            bases=('fancypages.contentblock', models.Model),
        ),
    ]
