""" Utils for core_parser_app fixtures
"""
from django.contrib.auth.models import User

from core_parser_app.components.data_structure.models import DataStructure
from tests import rights


class MockDataStructure(DataStructure):
    """MockDataStructure"""

    @staticmethod
    def get_permission():
        return f"{rights.tests_content_type}.{rights.mock_data_structure_access}"


class MockAnonDataStructure(DataStructure):
    """MockAnonDataStructure"""

    @staticmethod
    def get_permission():
        return f"{rights.tests_content_type}.{rights.mock_anon_data_structure_access}"


def create_user(
    username,
    password=None,
    email=None,
    is_staff=False,
    is_superuser=False,
):
    """Create a user

    Args:
        username:
        password:
        email:
        is_staff:
        is_superuser:

    Returns:

    """
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )

    user.save()
    return user
