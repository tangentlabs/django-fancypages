=========
Changelog
=========


0.3.1
-----

* Remove the ``target="_blank"`` attribute that used to be added by
  ``wysihtml5`` when sanitising link tags.
* Rename the ``advance.js`` config file for ``wysihtml5`` to
  ``wysihtml5-config.js``.
* Minify ``wysihtml5-config.js`` used for customising ``wyshtmls5`` to
  reduce size.


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
