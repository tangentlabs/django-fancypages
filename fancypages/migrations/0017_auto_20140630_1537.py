# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '0016_videoblock'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagenavigationblock',
            name='origin',
            field=models.CharField(default='absolute', max_length=50, verbose_name='navigation origin', choices=[('absolute', 'Start from top-level pages'), ('relative-siblings', 'Start from siblings'), ('relative-children', 'Start from children')]),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='pagenavigationblock',
            name='is_relative',
        ),
    ]
