.. django-fancypages documentation master file, created by
   sphinx-quickstart on Mon Jul 15 13:51:19 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-fancypages's documentation!
=============================================

The core principle of *fancypages* (FP) is to provide the user with a way to
edit and enhance content without giving them too much control over style and
layout. The objective is to maintain the overall design of the website.

The project was born out of the need to add content editing capabilities to an
e-commerce project based on `django-oscar`_.

.. warning::

   **Django 1.7** support is currently only available for the standalone
   version of fancypages. The ``fancypages.contrib.oscar_fancypages``
   integration package doesn't support it yet because `django-oscar`_ doesn't
   support it yet which makes it impossible to create migrations for
   ``oscar_fancypages``.


.. _`django-oscar`: https://github.com/tangentlabs/django-oscar

Contents:

.. toctree::
   :maxdepth: 2

   installation
   concepts 
   recipes
   contributing
   reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

