=======================================
Fancy CMS-style page editing for Django
=======================================

.. image:: https://travis-ci.org/tangentlabs/django-fancypages.png?branch=master
    :target: https://travis-ci.org/tangentlabs/django-fancypages?branch=master

.. image:: https://coveralls.io/repos/tangentlabs/django-fancypages/badge.png?branch=master
    :target: https://coveralls.io/r/tangentlabs/django-fancypages?branch=master

.. image:: https://requires.io/github/tangentlabs/django-fancypages/requirements.png?branch=refactoring
   :target: https://requires.io/github/tangentlabs/django-fancypages/requirements/?branch=refactoring
   :alt: Requirements Status


**Note:** This is a work in progress and part of this project will likely
change and could potentially break things. Be careful with using it.


Fancypages provides an easy way to edit content in your Django project.

Another content management system, you ask? No it is not! Rather, it is a
*content enhancement system* (CEnS) because it provides a user with the
controlled ability to edit content on a page.

The way this Django app works is inspired by `django-frontend-admin`_,
`django-content-blocks`_ and other similar apps. Especially, the use of
template tags to define customisable sections in a Django template is
based on the ideas in the two apps mentioned above.

**Warning:** There's currently an issue with *django-model-utils* 2.0+ and
Django 1.5.5. Until this is resolved, we advise to use **version 1.5** with
that specific version of Django.

.. _`django-frontend-admin`: https://github.com/bartTC/django-frontendadmin
.. _`django-content-blocks`: https://github.com/KevinBrolly/django-content-blocks


Oscar and Fancypages
--------------------

Fancypages has originally been developed to extend the functionality of
`django-oscar`_ by giving a the client limited control over content editing and
complement the Oscar dashboard. The need of other (non-Oscar) projects for a
similiar content editing funtionality lead to the separation of
`django-oscar-fancypages`_ into a separate app.

After several months of experience with maintaining both apps separately, we've
made the decision to maintain the Oscar integration as part of fancypages
available in ``fancypages.contrib.oscar_fancypages``. This should make it
easier to maintain both code bases and provide better integration for both.

**Note:** `django-oscar-fancypages`_ is now deprectated and will no longer
receive feature updates.


Screenshots
-----------

.. image:: https://raw.github.com/tangentlabs/django-fancypages/master/docs/source/images/screenshots/homepage_editor_hidden.png

.. image:: https://raw.github.com/tangentlabs/django-fancypages/master/docs/source/images/screenshots/homepage_editor_opened.png

.. image:: https://raw.github.com/tangentlabs/django-fancypages/master/docs/source/images/screenshots/homepage_edit_block_form.png

.. image:: https://raw.github.com/tangentlabs/django-fancypages/master/docs/source/images/screenshots/homepage_block_menu.png


Documentation
-------------

Installation instructions and documentation are hosted on the incredible 
`readthedocs.org`_:

    https://django-fancypages.readthedocs.org

.. _`readthedocs.org`: http://readthedocs.org


Projects Using Fancypages
-------------------------

* The Chocolate Box: https://www.chocolatebox.com.au
* Which Right Choice: https://www.whichrightchoice.com
* Freetix: https://www.freetix.com.au
* Agatha Christie: http://www.agathachristie.com

License
-------

``django-fancypages`` is released under the permissive `New BSD license`_.

.. _`New BSD license`: https://github.com/tangentlabs/django-fancypages/blob/master/LICENSE


.. image:: https://d2weczhvl823v0.cloudfront.net/tangentlabs/django-fancypages/trend.png
