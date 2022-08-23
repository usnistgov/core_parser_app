"""Module models
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions


class Module(models.Model):
    """Represents a module, that will replace the default rendering of an element"""

    name = models.CharField(unique=True, max_length=200)
    url = models.CharField(unique=True, max_length=200)
    view = models.CharField(max_length=200)
    multiple = models.BooleanField(default=False)

    @staticmethod
    def get_by_id(module_id):
        """Returns a module by its id

        Args:
            module_id:

        Returns:

        """
        try:
            return Module.objects.get(pk=str(module_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_by_url(module_url):
        """Returns a module by its id

        Args:
            module_url:

        Returns:

        """
        try:
            return Module.objects.get(url=module_url)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_all():
        """Returns all modules

        Returns:

        """
        return Module.objects.all()

    @staticmethod
    def get_all_urls():
        """Returns all modules urls

        Returns:

        """
        return Module.objects.all().values_list("url", flat=True)

    @staticmethod
    def delete_all():
        """Deletes all modules

        Returns:

        """
        Module.objects.all().delete()

    def __str__(self):
        """Module as string

        Returns:

        """
        return self.url
