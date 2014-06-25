# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oscar_fancypages', '0001_initial'),
        ('fancypages', '__first__'),
        ('offer', '__first__'),
        ('promotions', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, to_field='id', serialize=False, to='fancypages.ContentBlock')),
                ('offer', models.ForeignKey(verbose_name='Offer', to_field='id', to='offer.ConditionalOffer', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('fancypages.contentblock',),
        ),
        migrations.CreateModel(
            name='HandPickedProductsPromotionBlock',
            fields=[
                ('contentblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, to_field='id', serialize=False, to='fancypages.ContentBlock')),
            ],
            options={
                'abstract': False,
            },
            bases=('fancypages.contentblock',),
        ),
    ]
