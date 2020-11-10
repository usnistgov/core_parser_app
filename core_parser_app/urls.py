""" Url router for the parser application
"""
from django.conf.urls import include
from django.urls import re_path

from core_parser_app.views.common import views as common_views, ajax as common_ajax
from core_parser_app.views.user import ajax as user_ajax

urlpatterns = [
    re_path(
        r"^data-structure-element/value",
        user_ajax.data_structure_element_value,
        name="core_parser_app_data_structure_element_value",
    ),
    re_path(
        r"^template/modules/(?P<pk>\w+)",
        common_views.ManageModulesUserView.as_view(
            back_to_previous_url="core_main_app_manage_template_versions",
        ),
        name="core_parser_app_template_modules",
    ),
    re_path(
        r"^template/module/delete",
        common_ajax.delete_module,
        name="core_parser_app_delete_template_module",
    ),
    re_path(
        r"^template/module/insert",
        common_ajax.insert_module,
        name="core_parser_app_insert_template_module",
    ),
    re_path(r"^modules/", include("core_parser_app.tools.modules.urls")),
]
