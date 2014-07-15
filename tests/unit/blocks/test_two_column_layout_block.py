# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.test import TestCase
from django.test import RequestFactory
from django.template import RequestContext

from fancypages.models import Container
from fancypages.models.blocks import TwoColumnLayoutBlock

from fancypages.test import factories


class TestTwoColumnLayoutBlock(TestCase):

    def setUp(self):
        super(TestTwoColumnLayoutBlock, self).setUp()
        self.user = factories.UserFactory.build()

        self.request = RequestFactory().get('/')
        self.request_context = RequestContext(self.request, {})
        self.request_context['user'] = self.user

    def test_generates_two_empty_containers_when_rendered(self):
        container = Container.objects.create(name='test-container')
        block = TwoColumnLayoutBlock.objects.create(container=container)

        self.assertEquals(block.containers.count(), 0)
        renderer = block.get_renderer_class()(block, self.request_context)
        renderer.render()

        self.assertEquals(block.containers.count(), 2)
