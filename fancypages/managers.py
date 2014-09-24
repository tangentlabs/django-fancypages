# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import django

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

    def get_queryset(self):
        """
        The default queryset ordering the pages by the node paths to make sure
        that they are returned in the order they are in the tree.

        :rtype: QuerySet
        """
        return self.get_select_related_queryset().order_by('node__path')

    def get_query_set(self):
        """
        Method for backwards compatability only. Support for ``get_query_set``
        will be dropped in Django 1.8.
        """
        return self.get_queryset()

    def top_level(self):
        """
        Returns only the top level pages based on the depth provided in the
        page node.

        :rtype: QuerySet
        """
        return self.get_queryset().filter(node__depth=1)

    def visible(self, **kwargs):
        return self.get_select_related_queryset().visible(**kwargs)

    def visible_in(self, group):
        return self.get_select_related_queryset().visible_in(group=group)


class ContainerManager(models.Manager):

    def get_queryset(self):
        if django.VERSION[:2] == (1, 5):
            return super(ContainerManager, self).get_query_set()
        return super(ContainerManager, self).get_queryset()

    def get_language_query_set(self, **kwargs):
        if 'language_code' not in kwargs:
            kwargs['language_code'] = get_language()
        return self.get_queryset().filter(**kwargs)

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
        return self.get_queryset().get_or_create(**kwargs)
