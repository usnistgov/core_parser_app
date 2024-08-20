"""Module command unit testing
"""

from io import StringIO
from unittest.case import TestCase

from django.core.management import call_command


class TestLoadModulesCommand(TestCase):
    """Test Load Modules command"""

    def test_command_output(self):
        out = StringIO()
        call_command("loadmodules", stdout=out)
        self.assertIn("Modules were reloaded in database.", out.getvalue())
