# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...models import ContentBlock


Product = models.get_model('catalogue', 'Product')


class AbstractSingleProductBlock(ContentBlock):
    name = _("Single Product")
    code = 'single-product'
    group = _("Catalogue")
    template_name = "fancypages/blocks/productblock.html"

    product = models.ForeignKey(
        'catalogue.Product', verbose_name=_("Single Product"), null=True)

    def __unicode__(self):
        if self.product:
            return u"Product '{0}'".format(self.product.upc)
        return u"Product '{0}'".format(self.id)

    class Meta:
        abstract = True


class AbstractHandPickedProductsPromotionBlock(ContentBlock):
    name = _("Hand Picked Products Promotion")
    code = 'promotion-hand-picked-products'
    group = _("Catalogue")
    template_name = "fancypages/blocks/promotionblock.html"

    promotion = models.ForeignKey(
        'promotions.HandPickedProductList', null=True,
        verbose_name=_("Hand Picked Products Promotion"))

    def __unicode__(self):
        if self.promotion:
            return u"Promotion '{0}'".format(self.promotion.pk)
        return u"Promotion '{0}'".format(self.id)

    class Meta:
        abstract = True


class AbstractAutomaticProductsPromotionBlock(ContentBlock):
    name = _("Automatic Products Promotion")
    code = 'promotion-ordered-products'
    group = _("Catalogue")
    template_name = "fancypages/blocks/promotionblock.html"

    promotion = models.ForeignKey(
        'promotions.AutomaticProductList',
        verbose_name=_("Automatic Products Promotion"), null=True)

    def __unicode__(self):
        if self.promotion:
            return u"Promotion '{0}'".format(self.promotion.pk)
        return u"Promotion '{0}'".format(self.id)

    class Meta:
        abstract = True


class AbstractOfferBlock(ContentBlock):
    name = _("Offer Products")
    code = 'products-range'
    group = _("Catalogue")
    template_name = "fancypages/blocks/offerblock.html"

    offer = models.ForeignKey(
        'offer.ConditionalOffer', verbose_name=_("Offer"), null=True)

    @property
    def products(self):
        product_range = self.offer.condition.range
        if product_range.includes_all_products:
            return Product.browsable.filter(is_discountable=True)
        return product_range.included_products.filter(is_discountable=True)

    def __unicode__(self):
        if self.offer:
            return u"Offer '{0}'".format(self.offer.pk)
        return u"Offer '{0}'".format(self.id)

    class Meta:
        abstract = True


class AbstractPrimaryNavigationBlock(ContentBlock):
    name = _("Primary Navigation")
    code = 'primary-navigation'
    group = _("Content")
    template_name = "fancypages/blocks/primary_navigation_block.html"

    def __unicode__(self):
        return u'Primary Navigation'

    class Meta:
        abstract = True
