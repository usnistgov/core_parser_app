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


Migration to the Bootstrap modal
================================
Breaking changes during the migration from the jQuery UI modal to the Bootstrap modal for the module :

- The JavaScript global variables **openModule**, **openPopUp** and **initialState** from the popup.js file have been deleted.
- The JavaScript variable **openModule** has been renamed to **moduleElement**.
- The modal management has been changed. JQuery UI reused the same DOM element for all modal loaded in the page. Bootstrap use a unique DOM element for each modal. Consequently the main modal container will have the following unique ID : **modal-{{module_id}}**.
- The save callback uses the new variable **openModule** to get the unique DOM container and get the value to save.
- The Django form id must be changed be because it is not unique and can create conflict if the page includes a module more than one time (example with the BLOBHostForm):

.. code:: python

    form = BLOBHostForm()
    form.fields["file"].widget.attrs.update(
        {"id": "file-input-%s" % str(module_id)}
    )
