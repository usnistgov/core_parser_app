""" Data structure element model
"""

from bson.objectid import ObjectId
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions


class DataStructureElement(Document):
    """Represents data structure object"""

    user = fields.StringField()
    tag = fields.StringField()
    value = fields.StringField(blank=True)
    options = fields.DictField(default={}, blank=True)
    children = fields.ListField(fields.ReferenceField("self"), blank=True)

    @staticmethod
    def get_all_by_child_id(child_id, user=None):
        """Get Data structure element object which contains the given child id in its children

        Args:
            child_id:
            user:

        Returns:

        """
        try:
            if user is None:
                return DataStructureElement.objects(children=ObjectId(child_id)).all()
            else:
                return DataStructureElement.objects(
                    children=ObjectId(child_id), user=user
                ).all()
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_id(data_structure_element_id, user=None):
        """Returns the object with the given id

        Args:
            data_structure_element_id:
            user:

        Returns:
            DataStructureElement (obj): DataStructureElement object with the given id

        """
        try:
            if user is None:
                return DataStructureElement.objects.get(
                    pk=str(data_structure_element_id)
                )
            else:
                return DataStructureElement.objects.get(
                    pk=str(data_structure_element_id), user=user
                )
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_xpath(xpath, user=None):
        """Returns the object with the given id

        Args:
            xpath:
            user:

        Returns:
            DataStructureElement (obj): DataStructureElement object with the given id

        """

        try:
            if user is None:
                return DataStructureElement.objects(
                    __raw__={"options.xpath.xml": str(xpath)}
                )
            else:
                return DataStructureElement.objects(
                    __raw__={"options.xpath.xml": str(xpath)}, user=user
                )
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
