===============
Core Parser App
===============

XSD parser, renderers and modules for the curator core project.

Quick start
===========

1. Add "core_parser_app" to your INSTALLED_APPS setting
-------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
        ...
        "core_parser_app",
        "core_parser_app.tools.modules", 
        "core_parser_app.tools.parser", 
    ]

2. Include the core_parser_app URLconf in your project urls.py
--------------------------------------------------------------

.. code:: python

    url(r'^parser/', include("core_parser_app.urls")),

