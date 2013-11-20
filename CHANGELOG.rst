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


0.1.0
-----

The first public release.
