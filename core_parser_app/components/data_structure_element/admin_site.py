""" Custom admin site for the Data Structure Element model
"""
from django.contrib import admin


class CustomDataStructureElementAdmin(admin.ModelAdmin):
    """CustomDataStructureElementAdmin"""

    readonly_fields = ["tag", "parent", "data_structure"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Data Structure Elements"""
        return False
