=========
Changelog
=========

0.3.0
-----

* Provide the actual object for a block in the ``rendered_block`` tuples to
  allow more flexibility in the templates, especially in ``container.html``.

* Move the block selection modal markup from within the container into the
  body of the page. This means we only need a single modal including all
  available blocks. Also it avoids problems with displaying the modal.

* Switch the models for ``FancyPage`` and ``TreeNode`` to use Django's
  swappable API and loosen the relationship between the two. previously, the
  ``FancyPage`` model was a subclass of both the ``AbstractFancyPage`` and the
  ``AbstractTreeNode`` which caused issues in *django-oscar-fancypages* when
  integrating with the ``Category`` models. The use of the swappable API
  simplifies the handling of this relationship and makes customising the tree
  node used for the ``FancyPage`` easier.
  This adds two settings ``FP_NODE_MODEL`` for the tree node model class that
  will default to  ``fancypages.PageNode`` and the ``FP_PAGE_MODEL`` which 
  defaults to  ``fancypages.PageNode``.

* Interacting with blocks and containers has completely moved to the RESTful
  API for blocks and containers. This makes the use of AJAX calls to create,
  update and delete blocks more consistent. ``FancyPage`` models are still
  edited through the dashboard and are currently not available via the REST
  API.

* Fancypages provides a *Twitter* block that allows to specify a username and
  pull the user's twitter feed. This requires the ``twitter-tag`` django app
  which has caused issues before.  This requirement has now been removed and
  the *Twitter* block is now only available when the ``twitter-tag`` app is
  installed. If it is not, the block won't be registered with fancypages and
  won't be available to be added.

* UUIDs are now available on all models that are exposed via the REST API as
  well as the ``FancyPage`` model. This makes sure that content blocks,
  containers and pages are uniquely identifyable. This will support later
  features such as versioning and import/export.

* Major improvements to the integration tests to run Selenium test using
  saucelabs. It now covers a few fundamental use cases such as adding a new
  content block, deleting a content block and changing the content of a text
  block. The plan is to run these tests against various browser versions on
  saucelabs to make sure that the UI is working consistently on the most common
  browsers.

* Integrate `django-oscar-fancypages`_ as ``contrib`` package into fancypages.
  The main reasons for this decision was to ease maintainability for both
  projects and to avoid duplication between the two projects. The official
  integration of fancypages with Oscar now lives in
  ``fancypages.contrib.oscar_fancypages`` and should be used instead of the
  external package. As a result the configuration required to use fancypages
  in a standalone or an Oscar project has changed and will need to be updated
  when migrating from a previous installation. We have tried to provide full 
  backwards compatibility but there might be potential hickups in moving to
  this version of fancypages. If you come across any issues or use cases that
  we haven't anticipated, please open an issue on github.

* Containers in fancypages are now language aware by having a ``language_code``
  attribute that is available on the model. The language code **has** to be
  set and default to the ``LANGUAGE_CODE`` setting of your project. The main
  principle for dealing with multi-language sites is to have a separate
  container for each available language to allow total flexibility in setting
  up content for different languages. This might seem like a lot of additional
  work but there is a good reason for it. Different languages come with
  different cutural habits and experiences, e.g. what people in Britain might
  find hilarious might not work in the same way for people from Germany.
  Therefore, the content addressed to users speaking different languages often
  has to be adapted to work in the same or similar way. As a result we decided
  to allow complete freedom in the way the "same" content is presented for
  users speaking different languages. More details on this will be available in
  the docs.


.. _`django-oscar-fancypages`: https://github.com/tangentlabs/django-oscar-fancypages


0.1.0
-----

The first public release.
