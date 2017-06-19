# core_parser_app

core_parser_app is a Django app.

# Quick start

1. Add "core_parser_app" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
    ...
    "core_parser_app",
    "core_parser_app.tools.modules", 
    "core_parser_app.tools.parser", 
]
```

2. Include the core_parser_app URLconf in your project urls.py like this::

```python
url(r'^parser/', include("core_parser_app.urls")),
```