# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oscar_fancypages', '0002_handpickedproductspromotionblock_offerblock'),
        ('promotions', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='handpickedproductspromotionblock',
            name='promotion',
            field=models.ForeignKey(verbose_name='Hand Picked Products Promotion', to_field='id', to='promotions.HandPickedProductList', null=True),
            preserve_default=True,
        ),
    ]
