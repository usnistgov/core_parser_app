"""
Url router for the administration views
"""
from django.contrib import admin
from django.conf.urls import url
from views.admin import views as admin_views, ajax as admin_ajax


admin_urls = [
    url(r'^template/modules/(?P<template_id>\w+)', admin_views.manage_template_modules,
        name='core_parser_app_template_modules'),

    url(r'^template/module/delete', admin_ajax.delete_module,
        name='core_parser_app_delete_template_module'),
    url(r'^template/module/insert', admin_ajax.insert_module,
        name='core_parser_app_insert_template_module'),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
