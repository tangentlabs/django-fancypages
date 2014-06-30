# -*- coding: utf-8- -*-
from __future__ import absolute_import, unicode_literals

import pytest

from fancypages.test import factories
from fancypages.models import PageNavigationBlock


@pytest.fixture
def tree(db):
    """
    Fixture providing a tree of fancypages::

        + root
          + sibling1
            + child1
          + sibling2
            + child1
            + child2
    """
    root = factories.FancyPageFactory(node__name='root')
    sibling1 = factories.FancyPageFactory(
        node__name="node-1", node__parent=root)
    sibling2 = factories.FancyPageFactory(
        node__name="node-2", node__parent=root)
    factories.FancyPageFactory(node__name="node-1-1", node__parent=sibling1)
    factories.FancyPageFactory(node__name="node-2-1", node__parent=sibling2)
    factories.FancyPageFactory(node__name="node-2-2", node__parent=sibling2)
    return root


def test_page_navigation_block_return_empty_list_if_no_page():
    block = PageNavigationBlock()
    assert block.get_page_tree(None) == []


def test_nav_block_returns_tree_relative_to_children(tree):
    assert len(tree.get_children()) == 2

    block = PageNavigationBlock(
        origin=PageNavigationBlock.RELATIVE_FROM_CHILDREN)

    nav_tree = block.get_page_tree(tree.get_children()[0])
    assert len(nav_tree) == 1
    assert nav_tree[0][0].node.path == '000100010001'
    assert nav_tree[0][0].node.name == 'node-1-1'

    nav_tree = block.get_page_tree(tree.get_children()[1])
    assert len(nav_tree) == 2
    assert nav_tree[0][0].node.path == '000100020001'
    assert nav_tree[0][0].node.name == 'node-2-1'
    assert nav_tree[1][0].node.path == '000100020002'
    assert nav_tree[1][0].node.name == 'node-2-2'


@pytest.mark.parametrize('index', [0, 1])
def test_nav_block_returns_tree_relative_to_siblings(index, tree):
    block = PageNavigationBlock(
        origin=PageNavigationBlock.RELATIVE_FROM_SIBLINGS)

    nav_tree = block.get_page_tree(tree.get_children()[index])
    assert len(nav_tree) == 2
    assert nav_tree[0][0].node.path == '00010001'
    assert nav_tree[0][0].node.name == 'node-1'
    assert nav_tree[1][0].node.path == '00010002'
    assert nav_tree[1][0].node.name == 'node-2'


@pytest.mark.parametrize('depth', [2, 1])
def test_nav_block_returns_tree_absolute(depth, tree):
    block = PageNavigationBlock(
        depth=depth, origin=PageNavigationBlock.ABSOLUTE)
    nav_tree = block.get_page_tree(tree.get_children()[0])

    assert len(nav_tree) == 1
    assert nav_tree[0][0].node.path == '0001'
    assert nav_tree[0][0].node.name == 'root'

    if depth == 2:
        assert len(nav_tree[0]) == 2
        assert nav_tree[0][1][0][0].node.path == '00010001'
        assert nav_tree[0][1][0][0].node.name == 'node-1'
        assert nav_tree[0][1][1][0].node.path == '00010002'
        assert nav_tree[0][1][1][0].node.name == 'node-2'
