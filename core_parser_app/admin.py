"""
Url router for the administration views
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_parser_app.views.admin import views as admin_views

admin_urls = [
    re_path(
        r"^template/modules/(?P<pk>\w+)",
        staff_member_required(
            admin_views.ManageModulesAdminView.as_view(
                back_to_previous_url="admin:core_main_app_manage_template_versions",
            )
        ),
        name="core_parser_app_template_modules",
    ),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
