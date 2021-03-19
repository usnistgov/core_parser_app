""" Data structure element model
"""

from bson.objectid import ObjectId
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions


class DataStructureElement(Document):
    """Represents data structure object"""

    user = fields.StringField(blank=True)
    tag = fields.StringField()
    value = fields.StringField(blank=True)
    options = fields.DictField(default={}, blank=True)
    children = fields.ListField(fields.ReferenceField("self"), blank=True)
    data_structure = fields.GenericLazyReferenceField("DataStructure")

    @staticmethod
    def get_all_by_child_id(child_id):
        """Get Data structure element object which contains the given child id
        in its children.

        Args:
            child_id:

        Returns:

        """
        try:
            return DataStructureElement.objects(children=ObjectId(child_id)).all()
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all_by_child_id_and_user(child_id, user=None):
        """Get Data structure element object which contains the given child id
        in its children and an owner of the object.

        Args:
            child_id:
            user:

        Returns:

        """
        try:
            return DataStructureElement.objects(
                children=ObjectId(child_id), user=user
            ).all()
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_id(data_structure_element_id):
        """Returns the object with the given id.

        Args:
            data_structure_element_id:

        Returns:
            DataStructureElement (obj): DataStructureElement object with the given id

        """
        try:
            return DataStructureElement.objects.get(pk=str(data_structure_element_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_id_and_user(data_structure_element_id, user=None):
        """Returns the object with the given id and the given owner.

        Args:
            data_structure_element_id:
            user:

        Returns:
            DataStructureElement (obj): DataStructureElement object with the given id

        """
        try:
            return DataStructureElement.objects.get(
                pk=str(data_structure_element_id), user=user
            )
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_xpath(xpath):
        """Returns the object with the given id.

        Args:
            xpath:

        Returns:
            DataStructureElement (obj): DataStructureElement object with the given id

        """
        try:
            return DataStructureElement.objects(
                __raw__={"options.xpath.xml": str(xpath)}
            )
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_xpath_and_user(xpath, user=None):
        """Returns the object with the given id and owner.

        Args:
            xpath:
            user:

        Returns:
            DataStructureElement (obj): DataStructureElement object with the given id

        """
        try:
            return DataStructureElement.objects(
                __raw__={"options.xpath.xml": str(xpath)}, user=user
            )
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
