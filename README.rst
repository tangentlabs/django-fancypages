=======================================
Fancy CMS-style page editing for Django
=======================================

The idea of fanycpages is to provide some easy inline editing of pages. Another
content management system, you ask? Know it is not! We rather call it a content
enhancement system (CEnS) because it provides a user with a controlled
ability to edit content on a page.


Current Ideas
=============

* Call it django-tyler

Rendering tiles
---------------

* Tiles are the actual **models** containing the data.
* Their appearance is defined in the **renderer** which is similar to a
  form in core Django. Since we'll need attributes to be wrapped in some sort
  of HTML markup to use it with JS nicely it might make sense to implement a
  similar behaviour to form and model fields. Fields on the renderer are used
  to define the render type as which the field is rendered.
  For an actual export of the structure as HTML for use as a master page, it is
  necessary to provide a MasteringSerializer that adds the actual database field
  type as well. This should **never** be rendered into final HTML or cached
  HTML, though.

Serialiazers
------------

* There are several types of serializers that might make sense:
    ** render the whole page into HTML, dynamically
    ** render all widgets into a Django template. Tiles with static content are
        displayed as HTML. All the rest remains as an actual django template.
    ** Render the whole page into HTML but containing backend storage specific
        data so that containers and tiles can be generated from such a file.

* Rendering the template in multiple stages can be achieved through
  ``verbatim`` tags as in Django 1.5+. Tyler needs a compat implementation for
  this tag. This needs some eval and testing to figure out how to make a whole
  page verbatim and then exclude other rendered parts. The solution might be
  to render everything inside the container tag properly (unless specified) and
  for the main template including the tag(s), no actual rendering takes place.
  Not sure how that's going to work though.


Inspired by
===========

* django-frontend-admin
* django-content-blocks
