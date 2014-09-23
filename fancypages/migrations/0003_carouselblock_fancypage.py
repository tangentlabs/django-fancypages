# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import fancypages.assets.fields
from django.conf import settings
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '__first__'),
        ('fancypages', '0002_contentblock'),
        migrations.swappable_dependency(settings.FP_NODE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fancypages.ContentBlock')),
                ('link_url_1', models.CharField(max_length=500, null=True, verbose_name='Link URL 1', blank=True)),
                ('link_url_2', models.CharField(max_length=500, null=True, verbose_name='Link URL 2', blank=True)),
                ('link_url_3', models.CharField(max_length=500, null=True, verbose_name='Link URL 3', blank=True)),
                ('link_url_4', models.CharField(max_length=500, null=True, verbose_name='Link URL 4', blank=True)),
                ('link_url_5', models.CharField(max_length=500, null=True, verbose_name='Link URL 5', blank=True)),
                ('link_url_6', models.CharField(max_length=500, null=True, verbose_name='Link URL 6', blank=True)),
                ('link_url_7', models.CharField(max_length=500, null=True, verbose_name='Link URL 7', blank=True)),
                ('link_url_8', models.CharField(max_length=500, null=True, verbose_name='Link URL 8', blank=True)),
                ('link_url_9', models.CharField(max_length=500, null=True, verbose_name='Link URL 9', blank=True)),
                ('link_url_10', models.CharField(max_length=500, null=True, verbose_name='Link URL 10', blank=True)),
                ('image_1', fancypages.assets.fields.AssetKey(related_name=b'+', verbose_name='Image 1', blank=True, to='assets.ImageAsset', null=True)),
                ('image_2', fancypages.assets.fields.AssetKey(related_name=b'+', verbose_name='Image 2', blank=True, to='assets.ImageAsset', null=True)),
                ('image_3', fancypages.assets.fields.AssetKey(related_name=b'+', verbose_name='Image 3', blank=True, to='assets.ImageAsset', null=True)),
                ('image_4', fancypages.assets.fields.AssetKey(related_name=b'+', verbose_name='Image 4', blank=True, to='assets.ImageAsset', null=True)),
                ('image_5', fancypages.assets.fields.AssetKey(related_name=b'+', verbose_name='Image 5', blank=True, to='assets.ImageAsset', null=True)),
                ('image_6', fancypages.assets.fields.AssetKey(related_name=b'+', verbose_name='Image 6', blank=True, to='assets.ImageAsset', null=True)),
                ('image_7', fancypages.assets.fields.AssetKey(related_name=b'+', verbose_name='Image 7', blank=True, to='assets.ImageAsset', null=True)),
                ('image_8', fancypages.assets.fields.AssetKey(related_name=b'+', verbose_name='Image 8', blank=True, to='assets.ImageAsset', null=True)),
                ('image_9', fancypages.assets.fields.AssetKey(related_name=b'+', verbose_name='Image 9', blank=True, to='assets.ImageAsset', null=True)),
                ('image_10', fancypages.assets.fields.AssetKey(related_name=b'+', verbose_name='Image 10', blank=True, to='assets.ImageAsset', null=True)),
            ],
            options={
            },
            bases=('fancypages.contentblock',),
        ),
        migrations.CreateModel(
            name='FancyPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', shortuuidfield.fields.ShortUUIDField(db_index=True, verbose_name='Unique ID', max_length=22, editable=False, blank=True)),
                ('node', models.OneToOneField(related_name=b'page', null=True, verbose_name='Tree node', to=settings.FP_NODE_MODEL)),
                ('page_type', models.ForeignKey(related_name=b'pages', verbose_name='Page type', blank=True, to='fancypages.PageType', null=True)),
                ('keywords', models.CharField(max_length=255, verbose_name='Keywords', blank=True)),
                ('status', models.CharField(blank=True, max_length=15, verbose_name='Status', choices=[('published', 'Published'), ('draft', 'Draft'), ('archived', 'Archived')])),
                ('date_visible_start', models.DateTimeField(null=True, verbose_name='Visible from', blank=True)),
                ('date_visible_end', models.DateTimeField(null=True, verbose_name='Visible until', blank=True)),
                ('groups', models.ManyToManyField(related_name=b'pages', verbose_name='Groups', to=b'fancypages.PageGroup')),
            ],
            options={
                'abstract': False,
                'swappable': b'FP_PAGE_MODEL',
            },
            bases=(models.Model,),
        ),
    ]
