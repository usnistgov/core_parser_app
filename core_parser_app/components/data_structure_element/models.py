""" Data structure element model
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions
from bson.objectid import ObjectId


class DataStructureElement(Document):
    """Represents data structure object"""
    tag = fields.StringField()
    value = fields.StringField(blank=True)
    options = fields.DictField(default={})
    children = fields.ListField(fields.ReferenceField('self'), blank=True)

    @staticmethod
    def get_all():
        """

        Returns:

        """
        return DataStructureElement.objects.all()

    @staticmethod
    def get_by_id(data_structure_element_id):
        """ Returns the object with the given id

        Args:
            data_structure_element_id:

        Returns:
            DataStructureElement (obj): DataStructureElement object with the given id

        """
        try:
            return DataStructureElement.objects.get(pk=str(data_structure_element_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    @staticmethod
    def get_all_by_children(children):
        """

        Args:
            children:

        Returns:

        """
        return DataStructureElement.objects(children=children).all()

    @staticmethod
    def get_by_child_id(child_id):
        """ Get Data structure element object which contains the given child id in its children

        Args:
            child_id:

        Returns:

        """
        try:
            return DataStructureElement.objects().get(children__contains=ObjectId(child_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)
