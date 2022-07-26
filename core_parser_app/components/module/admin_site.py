""" Custom admin site for the Module model
"""
from django.contrib import admin


class CustomModuleAdmin(admin.ModelAdmin):
    """CustomModuleAdmin"""

    readonly_fields = ["name", "url", "view"]
    exclude = ["multiple"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Modules"""
        return False
