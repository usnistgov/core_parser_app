"""
Url router for the administration views
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_main_app.admin import core_admin_site
from core_parser_app.components.data_structure.admin_site import (
    CustomDataStructureAdmin,
)
from core_parser_app.components.data_structure.models import DataStructure
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_parser_app.components.data_structure_element.admin_site import (
    CustomDataStructureElementAdmin,
)
from core_parser_app.components.module.admin_site import CustomModuleAdmin
from core_parser_app.components.module.models import Module
from core_parser_app.views.admin import views as admin_views

admin_urls = [
    re_path(
        r"^template/modules/(?P<pk>\w+)",
        staff_member_required(
            admin_views.ManageModulesAdminView.as_view(
                back_to_previous_url="core-admin:core_main_app_manage_template_versions",
            )
        ),
        name="core_parser_app_template_modules",
    ),
]

admin.site.register(DataStructureElement, CustomDataStructureElementAdmin)
admin.site.register(DataStructure, CustomDataStructureAdmin)
admin.site.register(Module, CustomModuleAdmin)
urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
