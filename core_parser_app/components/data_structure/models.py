""" Data structure model
"""
import logging
from abc import abstractmethod

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_parser_app.tasks import delete_branch_task

logger = logging.getLogger(__name__)


class DataStructureElement(models.Model):
    """Represents data structure object"""

    user = models.CharField(blank=True, null=True, max_length=200)
    tag = models.CharField(blank=False, max_length=200)
    value = models.TextField(blank=True, null=True)
    options = models.JSONField(default=dict, blank=True)
    parent = models.ForeignKey(
        "self",
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name="children",
    )
    data_structure = models.ForeignKey(
        "DataStructure", on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    creation_date = models.DateTimeField(auto_now_add=True)

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
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
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
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
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
            return DataStructureElement.objects.filter(
                options__xpath__xml=str(xpath)
            ).all()
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
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
            return DataStructureElement.objects.filter(
                options__xpath__xml=xpath, user=user
            ).all()
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def __str__(self):
        """Data Structure Element as string

        Returns:

        """
        return f"{self.tag} ({str(self.id)})"


class DataStructure(models.Model):
    """Stores data being entered and not yet curated"""

    user = models.CharField(blank=True, max_length=200)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=200)
    data_structure_element_root = models.ForeignKey(
        DataStructureElement, blank=True, null=True, on_delete=models.SET_NULL
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta"""

        unique_together = (
            "user",
            "template",
            "name",
        )

    @staticmethod
    @abstractmethod
    def get_permission():
        """get_permission"""

        raise NotImplementedError("Permission is not set")

    def get_object_permission(self):
        """get_object_permission"""

        # FIXME: temporary solution to query concrete children of abstract class
        # iterate concrete data structure classes
        for subclass in DataStructure.__subclasses__():
            if hasattr(self, subclass._meta.model_name):
                return subclass.get_permission()

        raise NotImplementedError("Permission is not set")

    @staticmethod
    def get_by_id(data_structure_id):
        """Returns the object with the given id

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
            except exceptions.DoesNotExist as exception:
                # data structure not found, continue search
                logger.warning(
                    "Dependency %s threw an exception: %s",
                    subclass.__name__,
                    str(exception),
                )

        # data structure found
        if data_structure is not None:
            # return data structure
            return data_structure

        # raise exception
        raise exceptions.DoesNotExist("No data structure found for the given id.")

    @classmethod
    def pre_delete(cls, sender, instance, **kwargs):
        """Pre delete operations

        Returns:

        """
        # Delete data structure elements
        instance.delete_data_structure_elements_from_root()

    def delete_data_structure_elements_from_root(self):
        """Delete all data structure elements from the root

        Returns:

        """
        if self.data_structure_element_root is not None:
            delete_branch_task.apply_async((str(self.data_structure_element_root.id),))

    def __str__(self):
        """Data Structure as string

        Returns:

        """
        return f"{self.name} ({str(self.id)})"
