# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import fancypages.mixins
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', shortuuidfield.fields.ShortUUIDField(db_index=True, verbose_name='Unique ID', max_length=22, editable=False, blank=True)),
                ('container', models.ForeignKey(to='fancypages.Container', to_field='id', verbose_name='Container')),
                ('display_order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': [b'display_order'],
            },
            bases=(fancypages.mixins.TemplateNamesModelMixin, models.Model),
        ),
    ]
