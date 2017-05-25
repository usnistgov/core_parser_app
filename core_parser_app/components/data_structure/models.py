""" Data structure model
"""
from django_mongoengine import fields, Document
from core_main_app.components.template.models import Template
from core_parser_app.components.data_structure_element.models import DataStructureElement
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions


class DataStructure(Document):
    """Stores data being entered and not yet curated"""
    user = fields.StringField()
    template = fields.ReferenceField(Template)
    name = fields.StringField(unique_with=['user', 'template'])
    data_structure_element_root = fields.ReferenceField(DataStructureElement, blank=True)

    meta = {'abstract': True}

    @staticmethod
    def get_by_id(data_structure_id):
        """ Returns the object with the given id

        Args:
            data_structure_id:

        Returns:
            Data Structure (obj): DataStructure object with the given id

        """
        # FIXME: temporary solution to query concrete children of abstract class
        # (https://github.com/MongoEngine/mongoengine/issues/741)
        data_structure = None
        # iterate concrete data structure classes
        for subclass in DataStructure.__subclasses__():
            try:
                # get data structure from concrete subclass
                data_structure = subclass.get_by_id(data_structure_id)
                # break if found
                break
            except:
                # data structure not found, continue search
                pass
        # data structure found
        if data_structure is not None:
            # return data structure
            return data_structure
        else:
            # raise exception
            raise exceptions.DoesNotExist("No data structure found for the given id.")

