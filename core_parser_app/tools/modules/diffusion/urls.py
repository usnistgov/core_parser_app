from django.conf.urls import patterns, url

urlpatterns = patterns('core_parser_app.tools.modules.diffusion.views',
    url(r'^periodic-table$', 'periodic_table_view',
        name='core_parser_app_diffusion_periodic_table'),
    url(r'^periodic-table-multiple$', 'periodic_table_multiple_view',
        name='core_parser_app_diffusion_periodic_table_multiple'),
    url(r'^periodic-table-multiple-short', 'periodic_table_multiple_view_short',
        name='core_parser_app_diffusion_periodic_table_short'),
    url(r'^upload-excel', 'upload_excel_view',
        name='core_parser_app_diffusion_excel_uploader'),
)
