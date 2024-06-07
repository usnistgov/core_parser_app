""" Parser tasks
"""

from celery import shared_task


from core_parser_app.system import api as system_api


@shared_task
def delete_branch_task(data_structure_element_root_id):
    """
    Args:
        data_structure_element_root_id: Data Structure Element Root id.
    """
    system_api.delete_branch_from_db(data_structure_element_root_id)


@shared_task
def delete_data_structure_task(data_structure_id):
    """
    Args:
        data_structure_id: Data Structure id
    """
    data_structure = system_api.get_data_structure_by_id(data_structure_id)
    data_structure.delete()
