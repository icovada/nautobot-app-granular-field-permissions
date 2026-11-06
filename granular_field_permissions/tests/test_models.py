"""Test ContentTypeRuleSet."""

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from nautobot.apps.testing import ModelTestCases, TestCase
from nautobot.dcim.models import Device, Manufacturer
from nautobot.extras.choices import CustomFieldTypeChoices
from nautobot.extras.models import CustomField

from granular_field_permissions import models
from granular_field_permissions.tests import fixtures


class TestContentTypeRuleSet(ModelTestCases.BaseModelTestCase):
    """Test ContentTypeRuleSet."""

    model = models.ContentTypeRuleSet

    @classmethod
    def setUpTestData(cls):
        """Create test data for ContentTypeRuleSet Model."""
        super().setUpTestData()
        # Create 3 objects for the model test cases.
        fixtures.create_ContentTypeRuleSet()

    def test_create_ContentTypeRuleSet_only_required(self):
        """Create with only required fields, and validate null description and __str__."""
        ContentTypeRuleSet = models.ContentTypeRuleSet.objects.create(name="Development")
        self.assertEqual(ContentTypeRuleSet.name, "Development")
        self.assertEqual(ContentTypeRuleSet.description, "")
        self.assertEqual(str(ContentTypeRuleSet), "Development")

    def test_create_ContentTypeRuleSet_all_fields_success(self):
        """Create ContentTypeRuleSet with all fields."""
        ContentTypeRuleSet = models.ContentTypeRuleSet.objects.create(name="Development", description="Development Test")
        self.assertEqual(ContentTypeRuleSet.name, "Development")
        self.assertEqual(ContentTypeRuleSet.description, "Development Test")


class TestContentTypeRuleSetValidation(TestCase):
    """Test ContentTypeRuleSet validation."""

    def test_protected_fields_validation(self):
        for model, field_name, valid in (
            (Manufacturer, "name", True),
            (Manufacturer, "nonexistent", False),
            (Manufacturer, "id", False),  # not editable
            (Manufacturer, "device_types", False),  # reverse relation
            (Manufacturer, "tags", False),  # many-to-many
            (Manufacturer, "_custom_field_data", False),  # protected per custom field instead
            (Device, "device_redundancy_group_priority", False),  # action exceeds ObjectPermission's limit
        ):
            with self.subTest(model=model.__name__, field_name=field_name):
                ruleset = models.ContentTypeRuleSet(
                    content_type=ContentType.objects.get_for_model(model), protected_fields=[field_name]
                )
                if valid:
                    ruleset.full_clean()
                else:
                    with self.assertRaises(ValidationError) as context:
                        ruleset.full_clean()
                    self.assertIn("protected_fields", context.exception.message_dict)

    def test_protected_custom_fields_validation(self):
        content_type = ContentType.objects.get_for_model(Device)
        for label, key in (("Foo", "foo"), ("Long", "a_custom_field_key_that_is_too_long")):
            custom_field = CustomField.objects.create(label=label, key=key, type=CustomFieldTypeChoices.TYPE_TEXT)
            custom_field.content_types.add(content_type)

        for key, valid in (
            ("foo", True),
            ("nonexistent", False),
            ("a_custom_field_key_that_is_too_long", False),  # action exceeds ObjectPermission's limit
        ):
            with self.subTest(key=key):
                ruleset = models.ContentTypeRuleSet(content_type=content_type, protected_custom_fields=[key])
                if valid:
                    ruleset.full_clean()
                else:
                    with self.assertRaises(ValidationError) as context:
                        ruleset.full_clean()
                    self.assertIn("protected_custom_fields", context.exception.message_dict)
