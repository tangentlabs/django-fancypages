# encoding: utf8
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations
import fancypages.mixins
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', shortuuidfield.fields.ShortUUIDField(db_index=True, verbose_name='Unique ID', max_length=22, editable=False, blank=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', models.SlugField(max_length=128, verbose_name='Slug')),
                ('template_name', models.CharField(max_length=255, verbose_name='Template name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=255)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('image', models.ImageField(upload_to=b'fancypages/pages', null=True, verbose_name='Image', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
            ],
            options={
                'abstract': False,
                'swappable': b'FP_NODE_MODEL',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', shortuuidfield.fields.ShortUUIDField(db_index=True, verbose_name='Unique ID', max_length=22, editable=False, blank=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', models.SlugField(max_length=128, null=True, verbose_name='Slug', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', shortuuidfield.fields.ShortUUIDField(db_index=True, verbose_name='Unique ID', max_length=22, editable=False, blank=True)),
                ('name', models.SlugField(verbose_name='Variable name', blank=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('language_code', models.CharField(default=settings.LANGUAGE_CODE, max_length=7, verbose_name='Language')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', to_field='id', null=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
            ],
            options={
                'unique_together': set([(b'name', b'content_type', b'object_id', b'language_code')]),
            },
            bases=(fancypages.mixins.TemplateNamesModelMixin, models.Model),
        ),
    ]
