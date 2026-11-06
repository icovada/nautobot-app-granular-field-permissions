"""Test ContentTypeRuleSet forms."""

from django.test import TestCase

from granular_field_permissions import forms


class ContentTypeRuleSetTest(TestCase):
    """Test ContentTypeRuleSet forms."""

    def test_specifying_all_fields_success(self):
        form = forms.ContentTypeRuleSetForm(
            data={
                "name": "Development",
                "description": "Development Testing",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_specifying_only_required_success(self):
        form = forms.ContentTypeRuleSetForm(
            data={
                "name": "Development",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_validate_name_ContentTypeRuleSet_is_required(self):
        form = forms.ContentTypeRuleSetForm(data={"description": "Development Testing"})
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["name"])
