"""Unit tests for views."""

from nautobot.apps.testing import ViewTestCases

from granular_field_permissions import models
from granular_field_permissions.tests import fixtures


class ContentTypeRuleSetViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the ContentTypeRuleSet views."""

    model = models.ContentTypeRuleSet
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
        fixtures.create_ContentTypeRuleSet()
