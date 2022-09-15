""" Custom admin site for the Data Structure model
"""
from django.contrib import admin


class CustomDataStructureAdmin(admin.ModelAdmin):
    """CustomDataStructureAdmin"""

    readonly_fields = ["template", "data_structure_element_root"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Data Structures"""
        return False
