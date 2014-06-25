# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fancypages', '__first__'),
        ('catalogue', '__first__'),
        ('promotions', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomaticProductsPromotionBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, to_field='id', serialize=False, to='fancypages.ContentBlock')),
                ('promotion', models.ForeignKey(verbose_name='Automatic Products Promotion', to_field='id', to='promotions.AutomaticProductList', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('fancypages.contentblock',),
        ),
        migrations.CreateModel(
            name='PrimaryNavigationBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, to_field='id', serialize=False, to='fancypages.ContentBlock')),
            ],
            options={
                'abstract': False,
            },
            bases=('fancypages.contentblock',),
        ),
        migrations.CreateModel(
            name='SingleProductBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, to_field='id', serialize=False, to='fancypages.ContentBlock')),
                ('product', models.ForeignKey(verbose_name='Single Product', to_field='id', to='catalogue.Product', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('fancypages.contentblock',),
        ),
    ]
