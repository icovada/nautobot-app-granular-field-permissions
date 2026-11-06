"""Test field permission enforcement."""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from nautobot.apps.change_logging import web_request_context
from nautobot.apps.testing import TestCase
from nautobot.dcim.models import Manufacturer
from nautobot.extras.choices import CustomFieldTypeChoices
from nautobot.extras.models import CustomField

from granular_field_permissions.models import ContentTypeRuleSet
from granular_field_permissions.validators import invalidate_protected_fields


class TestFieldPermissionValidator(TestCase):
    """Test that protected fields can only be changed with the matching `field_<name>` permission."""

    def setUp(self):
        super().setUp()
        content_type = ContentType.objects.get_for_model(Manufacturer)
        self.custom_field = CustomField.objects.create(
            label="Foo", key="foo", type=CustomFieldTypeChoices.TYPE_TEXT, default="initial"
        )
        self.custom_field.content_types.add(content_type)
        self.manufacturer = Manufacturer.objects.create(name="Acme", _custom_field_data={"foo": "initial"})
        self.ruleset = ContentTypeRuleSet.objects.create(
            content_type=content_type, protected_fields=["name"], protected_custom_fields=["foo"]
        )
        # Test transactions never commit, so the `on_commit` invalidation hook doesn't fire on its own.
        invalidate_protected_fields()

    def _save_as(self, user, obj):
        with web_request_context(user):
            obj.validated_save()

    def test_protected_field_change_without_permission_is_rejected(self):
        self.manufacturer.name = "Renamed"
        with self.assertRaises(ValidationError) as context:
            self._save_as(self.user, self.manufacturer)
        self.assertIn("name", context.exception.message_dict)

    def test_protected_field_change_with_permission_is_allowed(self):
        self.add_permissions("dcim.field_name_manufacturer")
        self.manufacturer.name = "Renamed"
        self._save_as(self.user, self.manufacturer)

    def test_permission_constraints_apply_to_stored_object(self):
        self.add_permissions("dcim.field_name_manufacturer", constraints={"name": "Other"})
        self.manufacturer.name = "Other"
        with self.assertRaises(ValidationError):
            self._save_as(self.user, self.manufacturer)

    def test_unprotected_field_change_is_allowed(self):
        self.manufacturer.description = "Changed"
        self._save_as(self.user, self.manufacturer)

    def test_superuser_bypasses_protection(self):
        superuser = get_user_model().objects.create_user(username="admin", is_superuser=True)
        self.manufacturer.name = "Renamed"
        self._save_as(superuser, self.manufacturer)

    def test_create_is_not_checked(self):
        self._save_as(self.user, Manufacturer(name="New"))

    def test_ruleset_change_takes_effect_after_commit(self):
        with self.captureOnCommitCallbacks(execute=True):
            self.ruleset.protected_fields = ["description"]
            self.ruleset.validated_save()

        self.manufacturer.name = "Renamed"
        self._save_as(self.user, self.manufacturer)
        self.manufacturer.description = "Changed"
        with self.assertRaises(ValidationError):
            self._save_as(self.user, self.manufacturer)

    def test_protected_custom_field_change_without_permission_is_rejected(self):
        self.manufacturer._custom_field_data["foo"] = "changed"
        with self.assertRaises(ValidationError) as context:
            self._save_as(self.user, self.manufacturer)
        self.assertIn("foo", str(context.exception.message_dict[NON_FIELD_ERRORS]))

    def test_protected_custom_field_change_with_permission_is_allowed(self):
        self.add_permissions("dcim.cf_foo_manufacturer")
        self.manufacturer._custom_field_data["foo"] = "changed"
        self._save_as(self.user, self.manufacturer)

    def test_custom_field_default_filled_by_nautobot_is_not_a_change(self):
        Manufacturer.objects.filter(pk=self.manufacturer.pk).update(_custom_field_data={})
        self.manufacturer.refresh_from_db()
        self.manufacturer.description = "Changed"
        self._save_as(self.user, self.manufacturer)
