""" Unit tests for `core_parser_app.tasks` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_parser_app import tasks as parser_tasks


class TestDeleteBranchTask(TestCase):
    """Unit tests for `delete_branch_task` task."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"data_structure_element_root_id": MagicMock()}

    @patch("core_parser_app.system.api")
    def test_system_api_delete_branch_from_db_called(
        self, mock_parser_system_api
    ):
        """test_system_api_delete_branch_from_db_called"""
        parser_tasks.delete_branch_task(**self.mock_kwargs)

        mock_parser_system_api.delete_branch_from_db.assert_called_with(
            self.mock_kwargs["data_structure_element_root_id"]
        )
