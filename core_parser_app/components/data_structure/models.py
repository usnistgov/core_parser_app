""" Data structure model
"""

from django_mongoengine import fields, Document
from core_main_app.components.template.models import Template
from core_parser_app.components.data_structure_element.models import DataStructureElement


class DataStructure(Document):
    """Stores data being entered and not yet curated"""
    user = fields.StringField()
    template = fields.ReferenceField(Template)
    name = fields.StringField(unique_with=['user', 'template'])
    data_structure_element_root = fields.ReferenceField(DataStructureElement, blank=True)

    meta = {'abstract': True}

