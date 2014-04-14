from . import abstract_models as am

from ...library import register_content_block


@register_content_block
class SingleProductBlock(am.AbstractSingleProductBlock):
    pass


@register_content_block
class HandPickedProductsPromotionBlock(
        am.AbstractHandPickedProductsPromotionBlock):
    pass


@register_content_block
class AutomaticProductsPromotionBlock(
        am.AbstractAutomaticProductsPromotionBlock):
    pass


@register_content_block
class OfferBlock(am.AbstractOfferBlock):
    pass


@register_content_block
class PrimaryNavigationBlock(am.AbstractPrimaryNavigationBlock):
    pass
