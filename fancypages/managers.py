from django.db import models
from django.utils.translation import get_language

from .queryset import PageQuerySet


class PageManager(models.Manager):

    def get_select_related_queryset(self):
        """
        Get the base query set that pulls the related ``PageNode`` whenever
        the page queryset is used. The reason for this is that the page node
        is essential and we don't want to have multiple queries every time.

        :rtype: QuerySet
        """
        return PageQuerySet(self.model).select_related('node')

    def get_query_set(self):
        """
        The default queryset ordering the pages by the node paths to make sure
        that they are returned in the order they are in the tree.

        :rtype: QuerySet
        """
        return self.get_select_related_queryset().order_by('node__path')

    def top_level(self):
        """
        Returns only the top level pages based on the depth provided in the
        page node.

        :rtype: QuerySet
        """
        return self.get_query_set().filter(node__depth=1)

    def visible(self, **kwargs):
        return self.get_select_related_queryset().visible(**kwargs)

    def visible_in(self, group):
        return self.get_select_related_queryset().visible_in(group=group)


class ContainerManager(models.Manager):

    def get_language_query_set(self, **kwargs):
        if 'language_code' not in kwargs:
            kwargs['language_code'] = get_language()
        return self.get_query_set().filter(**kwargs)

    def all(self):
        return self.get_language_query_set()

    def filter(self, **kwargs):
        return self.get_language_query_set(**kwargs)

    def create(self, **kwargs):
        if 'language_code' not in kwargs:
            kwargs['language_code'] = get_language()
        return super(ContainerManager, self).create(**kwargs)

    def get_or_create(self, **kwargs):
        if 'language_code' not in kwargs:
            kwargs['language_code'] = get_language()
        return self.get_query_set().get_or_create(**kwargs)
