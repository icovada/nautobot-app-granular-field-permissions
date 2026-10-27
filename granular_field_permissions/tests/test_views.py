"""Unit tests for views."""

from nautobot.apps.testing import ViewTestCases

from granular_field_permissions import models
from granular_field_permissions.tests import fixtures


class GranularFieldPermissionsExampleModelViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the GranularFieldPermissionsExampleModel views."""

    model = models.GranularFieldPermissionsExampleModel
    bulk_edit_data = {"description": "Bulk edit views"}
    form_data = {
        "name": "Test 1",
        "description": "Initial model",
    }

    update_data = {
        "name": "Test 2",
        "description": "Updated model",
    }

    @classmethod
    def setUpTestData(cls):
        fixtures.create_granularfieldpermissionsexamplemodel()
