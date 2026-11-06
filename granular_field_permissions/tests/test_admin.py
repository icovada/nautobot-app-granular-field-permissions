"""Test the ContentTypeRuleSet admin."""

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from nautobot.apps.testing import TestCase
from nautobot.dcim.models import Manufacturer
from nautobot.extras.choices import CustomFieldTypeChoices
from nautobot.extras.models import CustomField

from granular_field_permissions.models import ContentTypeRuleSet


class TestContentTypeRuleSetAdmin(TestCase):
    """Test creating and editing rulesets through the Django admin."""

    def setUp(self):
        super().setUp()
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.content_type = ContentType.objects.get_for_model(Manufacturer)

    def test_add_ruleset_with_comma_separated_fields(self):
        response = self.client.post(
            reverse("admin:granular_field_permissions_contenttyperuleset_add"),
            {"content_type": self.content_type.pk, "protected_fields": "name,description"},
        )
        self.assertEqual(response.status_code, 302)
        ruleset = ContentTypeRuleSet.objects.get(content_type=self.content_type)
        self.assertEqual(ruleset.protected_fields, ["name", "description"])

    def test_add_ruleset_rejects_unprotectable_field(self):
        response = self.client.post(
            reverse("admin:granular_field_permissions_contenttyperuleset_add"),
            {"content_type": self.content_type.pk, "protected_fields": "tags"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ContentTypeRuleSet.objects.exists())

    def test_change_form_offers_only_protectable_fields(self):
        custom_field = CustomField.objects.create(label="Foo", key="foo", type=CustomFieldTypeChoices.TYPE_TEXT)
        custom_field.content_types.add(self.content_type)
        ruleset = ContentTypeRuleSet.objects.create(content_type=self.content_type, protected_fields=["name"])
        response = self.client.get(
            reverse("admin:granular_field_permissions_contenttyperuleset_change", args=[ruleset.pk])
        )
        form_fields = response.context["adminform"].form.fields
        choices = [value for value, _ in form_fields["protected_fields"].choices]
        self.assertIn("name", choices)
        self.assertNotIn("tags", choices)
        self.assertNotIn("id", choices)
        self.assertNotIn("_custom_field_data", choices)
        custom_field_choices = [value for value, _ in form_fields["protected_custom_fields"].choices]
        self.assertEqual(custom_field_choices, ["foo"])
