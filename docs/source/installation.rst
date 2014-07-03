============
Installation
============

You can use *django-fancypages* as standalone app in your Django project or you
can integrate it with your `django-oscar`_ shop using the included extension
module. In the following sections, the standalone setup of django-fancypages
will be referred to as *FP* and the Oscar integration as *OFP*.

#Most of the installation steps are exactly the same for both so let's
#go through these steps first. After you have completed them, follow the 

.. note::

   The two sandbox sites in FP show an example integration
   with `django-oscar`_ and as standalone project. They both use
   `django-configurations`_ maintained by the awesome Jannis Leidel to make
   dealing with Django settings much simpler. Using it is not a requirement for
   *django-fancypages* it's just a personal preference. The following settings
   explain the setup using the basic Django ``settings.py`` but I recommend
   checking out *django-configurations*.


Installing Fancypages
---------------------

For both FP and OFP, you have to install the python package *django-fancypages*
which is available on PyPI and can be installed with:

.. code:: bash
   
    $ pip install django-fancypages

or you can install the latest version directly from `the github repo`_:

.. code:: bash

    $ pip install git+https://github.com/tangentlabs/django-fancypages.git


Standalone Setup
----------------

Let's start with adding all required apps to you ``INSTALLED_APPS``. FP relies
on several third-party apps in addition to the ``fancypages`` app itself. For
convenience, FP provides two functions ``get_required_apps`` and
``get_fancypages_apps`` that make it easy to add all apps in one additional 
line of code:

.. code-block:: python

    from fancypages import get_required_apps, get_fancypages_apps

    INSTALLED_APPS = [
        ...
    ] + get_required_apps() + get_fancypages_apps()


.. note::

    FP supports **Django 1.7** which replaces ``South`` migrations with a new
    migration system integrated in Django. The ``fancypages.migrations`` module
    containse the *new-style* migrations and will only work for Django 1.7+.  
    For **Django 1.5 and 1.6**, you have to add ``south`` to your installed
    apps and specify an alternative migrations module in the
    ``SOUTH_MIGRATION_MODULES`` settings. Add the following to your settings
    when using either of these versions::

        SOUTH_MIGRATION_MODULES = {
            'fancypages': "fancypages.south_migrations",
        }

    It will then behave in exactly the same way as before.


Next you have add a piece of middleware that provide the content editor
functionality on pages that are managed by FP. The content editor works similar
to `django-debug-toolbar`_ and uses the same middleware mechanism to inject
additional mark up into every FP-enabled page if the current user has admin
privileges. Add the FP middleware to the end of your ``MIDDLEWARE_CLASSES``:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'fancypages.middleware.EditorMiddleware',
    )


Fancypages requires several default settings to be added. To make sure
that you have all the default settings in your settings, you can use
the defaults provided by fancypages itself. Add the following in your
settings file **before** you overwrite specific settings:

.. code-block:: python

    ...
    from fancypages.defaults import *

    # override the defaults here (if required)
    ...

Finally, you have to add URLs to your ``urls.py`` to make the fancypages
dashboard and all FP-enabled pages available on your sight. FP uses a very
broad matching of URLs to ensure that you can have nicely nested URLs with your
pages. This will match **all** URLs it encounters, so make sure that you add
them as the very last entry in your URL patterns:

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^', include('fancypages.urls')),
    )


If you would like the home page of your project to be an FP-enabled page as
well, you have to add one additional URL pattern:

.. code-block:: python

    urlpatterns = patterns('',
        url(r'^$', views.HomeView.as_view(), name='home'),
        ...
        url(r'^', include('fancypages.urls')),
    )


This view behaves slightly different from a regular ``FancyPageView``: if no
:class:`FancyPage <fancypages.models.FancyPage>` instance exists with the name
``Home`` (and the corresponding slug ``home``), this page will be created
automatically as a "Draft" page. Make sure that you publish the page to be able
to see it as non-admin user.


Setup Alongside Oscar
---------------------

.. note::
    The following instructions assume that you have Oscar set up succesfully
    by following Oscar's documentation. Addressing Oscar-specific set up
    details aren't considered here. We recommend that you take a close look at
    Oscar's documentation before continuing.

Setting up *django-fancypages* alongside your `django-oscar`_ shop is very
similar to the standalone setup. You also have to add extra apps to your
``INSTALLED_APPS`` and once again, you can use the convenience function
provided by fancypages. Note that we pass ``use_with_oscar=True`` to ensure
that the ``fancypages.contrib.oscar_fancypages`` app is added:

.. code-block:: python

    from fancypages import get_required_apps, get_fancypages_apps

    INSTALLED_APPS = [
        ...
    ] + fp.get_required_apps() \
      + fp.get_fancypages_apps(use_with_oscar=True) \
      + get_core_apps()

.. note::

    Once again, FP ships the *new-style* migrations for Django 1.7+ by default.
    If you are using Django 1.5 or 1.6, you have to make sure that you have 
    ``south`` in your ``INSTALLED_APPS`` and add the following setting to point
    to the alternative South migrations::

        SOUTH_MIGRATION_MODULES = {
            'fancypages': "fancypages.south_migrations",
            'oscar_fancypages': 'fancypages.contrib.oscar_fancypages.south_migrations',  # noqa
        }

    You can now use ``syncdb`` and ``migrate`` as you would normally.


Next you have add a piece of middleware that provide the content editor
functionality on pages that are managed by FP. The content editor works similar
to `django-debug-toolbar`_ and uses the same middleware mechanism to inject
additional mark up into every FP-enabled page if the current user has admin
privileges. Add the FP middleware to the end of your ``MIDDLEWARE_CLASSES``:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'fancypages.middleware.EditorMiddleware',
    )

Similar to the standalone setup, you have to import the default settings for
FP in your ``settings.py``. However, to make the integration with Oscar
seamless, you have to set the ``FP_NODE_MODEL`` to Oscar's ``Category`` model.
The reason for this is, that categories in Oscar already provide a
tree-structure on the site that we can leverage. Switching the page node
from FP's internal model to Oscar's ``Category`` is as easy as:

.. code-block:: python

    ...
    from fancypages.defaults import *

    FP_NODE_MODEL = 'catalogue.Category'
    FP_PAGE_DETAIL_VIEW = 'fancypages.contrib.oscar_fancypages.views.FancyPageDetailView'
    ...

In addition, you should integrate the page management dashboard with Oscar's
builtin dashboard. We recommend replacing the entry "Catalogue > Categories"
with FP's page management by replacing:

.. code-block:: python

    OSCAR_DASHBOARD_NAVIGATION = [
        ...
            {
                'label': _('Categories'),
                'url_name': 'dashboard:catalogue-category-list',
            },
        ...
    ]

with: 

.. code-block:: python

    OSCAR_DASHBOARD_NAVIGATION = [
        ...
            {
                'label': _('Pages / Categories'),
                'url_name': 'fp-dashboard:page-list',
            },
        ...
    ]

This usually means, you have to copy the entire ``OSCAR_DASHBOARD_NAVIGATION``
dictionary from ``oscar.defaults`` to overwrite it with your own.

The last thing to configure is the URLs for the pages. Conceptually, a
:class:`FancyPage <fancypages.models.FancyPage>` is equivalent to a
``Category`` in Oscar, therefore, a ``FancyPage`` wraps the ``Category`` model
and adds FP-specific behaviour. Therefore, we have to modify Oscar's URLs to
replace the category URLs with those for our FP pages. This sounds more
complicated than it actually is:

.. code-block:: python

    from fancypages.app import application as fancypages_app
    from fancypages.contrib.oscar_fancypages import views

    from oscar.app import Shop
    from oscar.apps.catalogue.app import CatalogueApplication


    class FancyCatalogueApplication(CatalogueApplication):
        category_view = views.FancyPageDetailView


    class FancyShop(Shop):
        catalogue_app = FancyCatalogueApplication()


    urlpatterns = patterns('',
        ...
        url(r'', include(FancyShop().urls)),
        ...
        url(r'^', include(fancypages_app.urls)),
    )

All we are doing here is, replacing the ``CategoryView`` in Oscar with the
``FancyPageDetailView`` from OFP, which will display the same details as
Oscar's template.

Replacing the home page with a FP page works exactly the same way as described
in `Standalone Setup`.


Running Migrations
------------------

Before you are ready to go, make sure that you've applied the migrations for
FP and OFP (depending on your setup) by running:

.. code:: bash

    $ ./manage.py migrate


.. _`django-oscar`: http://django-oscar.readthedocs.org
.. _`django-debug-toolbar`: http://django-debug-toolbar.readthedocs.org
.. _`django-configurations`: http://django-configurations.readthedocs.org
.. _`the github repo`: https://github.com/tangentlabs/django-fancypages/tree/master/fancypages
