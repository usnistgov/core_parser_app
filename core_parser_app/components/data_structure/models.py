""" Data structure model
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_parser_app.components.data_structure_element.models import DataStructureElement


# FIXME: no direct link to XML data (make the link only in curate app)
# FIXME: xml_data = dme_fields.StringField(default='')
# FIXME: xml_data_id = dme_fields.StringField(blank=True)

class DataStructure(Document):
    """Stores data being entered and not yet curated"""
    user = fields.StringField()
    template = fields.ReferenceField(Template)
    name = fields.StringField(unique_with=['user', 'template'])
    data_structure_element_root = fields.ReferenceField(DataStructureElement, blank=True)

    @staticmethod
    def get_by_id(data_structure_id):
        """ Returns the object with the given id

        Args:
            data_structure_id:

        Returns:
            DataStructure (obj): DataStructureElement object with the given id

        """
        try:
            return DataStructure.objects.get(pk=str(data_structure_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)
