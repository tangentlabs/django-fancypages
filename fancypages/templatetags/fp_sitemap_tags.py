from django import template
from django.db.models import get_model


VisibilityType = get_model('fancypages', 'VisibilityType')
FancyPage = get_model('fancypages', 'FancyPage')
Category = get_model('catalogue', 'Category')


register = template.Library()

INSTANCE_TYPE_CATEGORY = 'category'
INSTANCE_TYPE_PAGE = 'page'
INSTANCE_TYPES = (
    INSTANCE_TYPE_CATEGORY,
    INSTANCE_TYPE_PAGE
)


def build_tree(root, parent, data, depth, instance_type):
    for instance in data[depth]:
        if instance_type == INSTANCE_TYPE_CATEGORY:
            category = instance
        else:
            category = instance.category
        if not parent or category.is_child_of(parent):
            node = (instance, [])
            if depth < len(data) - 1:
                build_tree(node[1], category, data, depth + 1, instance_type)
            root.append(node)
    return root


@register.assignment_tag
def get_pages(visibility_type):
    try:
        visibility_type_instance = VisibilityType.objects.get(
            slug=visibility_type
        )
    except VisibilityType.DoesNotExist:
        return FancyPage.objects.none()
    return FancyPage.objects.visible_in(visibility_type_instance)


@register.assignment_tag
def get_site_tree(visibility_type=None, depth=1,
                  instance_type=INSTANCE_TYPE_PAGE):
    if instance_type not in INSTANCE_TYPES:
        return []

    try:
        visibility_type_instance = VisibilityType.objects.get(
            slug=visibility_type
        )
    except VisibilityType.DoesNotExist:
        visibility_type_instance = None
        if visibility_type:
            return []

    categories = Category.objects.filter(depth__lte=depth)
    if visibility_type_instance:
        categories = categories.filter(
            page__visibility_types=visibility_type_instance
        )

    category_buckets = [[] for i in range(depth)]

    for c in categories:
        instance = c if instance_type == INSTANCE_TYPE_CATEGORY else c.page
        category_buckets[c.depth - 1].append(instance)
    category_subtree = []

    build_tree(category_subtree, None, category_buckets, 0, instance_type)

    return category_subtree
