from django.conf.urls import url

import views

urlpatterns = [
    url(r'^periodic-table$', views.periodic_table_view,
        name='core_parser_app_diffusion_periodic_table'),
    url(r'^periodic-table-multiple$', views.periodic_table_multiple_view,
        name='core_parser_app_diffusion_periodic_table_multiple'),
    url(r'^periodic-table-multiple-short', views.periodic_table_multiple_view_short,
        name='core_parser_app_diffusion_periodic_table_short'),
    url(r'^upload-excel', views.upload_excel_view,
        name='core_parser_app_diffusion_excel_uploader'),
]
