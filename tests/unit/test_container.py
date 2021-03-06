# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import pytest

from django.template import RequestContext
from django.test import RequestFactory
from django.contrib.auth.models import User

from fancypages.test import factories
from fancypages.models import Container
from fancypages.renderers import ContainerRenderer


@pytest.fixture
def request_context():
    request = RequestFactory().get('/')
    request.fp_edit_mode = True
    request.user = User()
    return RequestContext(request, {})


def test_container_can_be_retrieved_by_name(request_context, db):
    container = Container.objects.create(name='some-container')
    retrieved_container = Container.get_container_by_name(container.name)
    assert container.id == retrieved_container.id


def test_renders_block_selection_correctly(request_context, db):
    ctn_id = 15
    container = factories.ContainerFactory.build(id=ctn_id)
    html = ContainerRenderer(container, request_context).render()

    assert 'data-target="#block_selection_modal"'.format(container.uuid) in html  # noqa
    assert 'data-container-id="{}"'.format(container.uuid) in html


def test_container_generates_a_name_based_on_specified_uuid(db):
    container = Container.objects.create(uuid='fakeuuid')
    assert container.name == "container-fakeuuid"


def test_container_generates_a_name_based_on_autogenerated_uuid(db):
    container = Container.objects.create()
    assert container.uuid is not None
    assert container.name == "container-{}".format(container.uuid)


def test_object_container_can_be_retrieved_by_name(db):
    user = User.objects.create(username='testuser')
    container = Container.objects.create(
        name='some-container', page_object=user)

    retrieved_container = Container.get_container_by_name(container.name, user)
    assert container.id == retrieved_container.id
