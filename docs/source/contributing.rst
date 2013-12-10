============
Contributing
============


Integration Tests
-----------------

The test that are based on Django's ``LiveServerTestCase`` are considered
integration test. We use `splinter`_ that runs on top of `Selenium`_ for that.
All integration tests are based on the ``SplinterTestCase
<fancypages.test.testcases.SplinterTestCase>`` and carry the py.test marker
``integration`` that is excluded from the default running of tests. To run
integration tests run::

    py.test -m integration

There are a couple of settings that allow changes to the way selenium/splinter
is run. Setting ``SPLINTER_WEBDRIVER`` to a valid Selenium webdriver allows
for changing the default webdriver to whatever you want (assuming the required
driver is installed). Another helpful variable is ``SPLINTER_DEBUG`` which
prevents the Selenium browser from being closed after finishing a test run so
you can inspect the state of the site. Using both settings a test could be run
like this::

    SPLINTER_DEBUG=true SPLINTER_WEBDRIVER=chrome py.test -m integration


.. _`splinter`: http://splinter.cobrateam.info
.. _`Selenium`: https://code.google.com/p/selenium/
