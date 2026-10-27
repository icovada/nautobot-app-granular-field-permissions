"""Test GranularFieldPermissionsExampleModel."""

from nautobot.apps.testing import ModelTestCases

from granular_field_permissions import models
from granular_field_permissions.tests import fixtures


class TestGranularFieldPermissionsExampleModel(ModelTestCases.BaseModelTestCase):
    """Test GranularFieldPermissionsExampleModel."""

    model = models.GranularFieldPermissionsExampleModel

    @classmethod
    def setUpTestData(cls):
        """Create test data for GranularFieldPermissionsExampleModel Model."""
        super().setUpTestData()
        # Create 3 objects for the model test cases.
        fixtures.create_granularfieldpermissionsexamplemodel()

    def test_create_granularfieldpermissionsexamplemodel_only_required(self):
        """Create with only required fields, and validate null description and __str__."""
        granularfieldpermissionsexamplemodel = models.GranularFieldPermissionsExampleModel.objects.create(name="Development")
        self.assertEqual(granularfieldpermissionsexamplemodel.name, "Development")
        self.assertEqual(granularfieldpermissionsexamplemodel.description, "")
        self.assertEqual(str(granularfieldpermissionsexamplemodel), "Development")

    def test_create_granularfieldpermissionsexamplemodel_all_fields_success(self):
        """Create GranularFieldPermissionsExampleModel with all fields."""
        granularfieldpermissionsexamplemodel = models.GranularFieldPermissionsExampleModel.objects.create(name="Development", description="Development Test")
        self.assertEqual(granularfieldpermissionsexamplemodel.name, "Development")
        self.assertEqual(granularfieldpermissionsexamplemodel.description, "Development Test")
