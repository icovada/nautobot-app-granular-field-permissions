"""Field-level edit permissions, enforced through runtime-registered Nautobot CustomValidators."""

import uuid
from typing import NamedTuple

from django.core.cache import cache
from django.core.exceptions import NON_FIELD_ERRORS
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from nautobot.apps.models import CustomValidator
from nautobot.apps.utils import FeatureQuery
from nautobot.extras.models import CustomField
from nautobot.extras.plugins import register_custom_validators

from granular_field_permissions.models import (
    ContentTypeRuleSet,
    custom_field_permission_action,
    field_permission_action,
)

PROTECTED_FIELDS_VERSION_KEY = "granular_field_permissions:protected_fields_version"

# Per-process copy of all rulesets, rebuilt whenever the version token in the shared cache changes.
_protected_fields = {"version": None, "by_model": {}}


class ProtectedFields(NamedTuple):
    """Field names and custom field keys protected on one model."""

    fields: frozenset[str]
    custom_fields: frozenset[str]


def get_protected_fields() -> dict[str, ProtectedFields]:
    """Return protected fields keyed by model label, querying the database only after a ruleset changed."""
    version = cache.get_or_set(PROTECTED_FIELDS_VERSION_KEY, lambda: uuid.uuid4().hex, timeout=None)
    if version != _protected_fields["version"]:
        _protected_fields["by_model"] = {
            f"{app_label}.{model}": ProtectedFields(frozenset(fields), frozenset(custom_fields))
            for app_label, model, fields, custom_fields in ContentTypeRuleSet.objects.values_list(
                "content_type__app_label", "content_type__model", "protected_fields", "protected_custom_fields"
            )
        }
        _protected_fields["version"] = version
    return _protected_fields["by_model"]


def invalidate_protected_fields():
    """Make every process rebuild its protected fields on the next `get_protected_fields()` call."""
    cache.set(PROTECTED_FIELDS_VERSION_KEY, uuid.uuid4().hex, timeout=None)


@receiver(post_save, sender=ContentTypeRuleSet)
@receiver(post_delete, sender=ContentTypeRuleSet)
def _invalidate_on_ruleset_change(**kwargs):
    # On commit, so no process can rebuild from pre-commit data and cache it under the new version.
    transaction.on_commit(invalidate_protected_fields)


def build_custom_validator(model: str, clean_func, name: str) -> type[CustomValidator]:
    """Build a `CustomValidator` subclass in memory.

    Args:
        model: Model label in the form `<app_label>.<model_name>`, e.g. `dcim.manufacturer`.
        clean_func: Function taking the validator instance as `self`. The object under validation is
            `self.context["object"]`; raise `ValidationError` (e.g. via `self.validation_error()`) to reject it.
        name: Class name of the generated validator.
    """
    return type(name, (CustomValidator,), {"model": model.lower(), "clean": clean_func, "__module__": __name__})


def _stored_custom_field_value(stored_data, key):
    """Return the value of custom field `key` an unchanged object would hold after Nautobot's own `clean()`."""
    if key in stored_data:
        return stored_data[key]
    # Nautobot's `clean()` runs before validators and fills keys missing from older objects with the default.
    return CustomField.objects.filter(key=key).values_list("default", flat=True).first()


def _check_field_permissions(self):
    """Reject edits to protected fields and custom fields the user hasn't been granted the matching action for.

    Permission constraints are evaluated against the stored object, like any `ObjectPermission`. Creation is
    governed by the regular `add_<model>` permission and isn't checked here.
    """
    obj = self.context["object"]
    user = self.context["user"]
    if obj._state.adding or user.is_superuser:
        return
    meta = obj._meta
    protected = get_protected_fields().get(meta.label_lower)
    if protected is None:
        return

    # Fields dropped from the model since the ruleset was saved are ignored rather than breaking every save.
    fields = [field for field in meta.concrete_fields if field.name in protected.fields]
    columns = [field.attname for field in fields]
    if protected.custom_fields:
        columns.append("_custom_field_data")
    if not columns:
        return
    original = meta.base_manager.filter(pk=obj.pk).values(*columns).first()
    if original is None:
        return

    def has_action(action):
        return user.has_perm(f"{meta.app_label}.{action}_{meta.model_name}", obj)

    errors = {
        field.name: "You do not have permission to change this field."
        for field in fields
        if getattr(obj, field.attname) != original[field.attname]
        and not has_action(field_permission_action(field.name))
    }
    # Custom field values aren't form fields of the model, so like Nautobot's own custom field errors these
    # are reported as non-field errors.
    custom_field_errors = [
        f"You do not have permission to change custom field '{key}'."
        for key in sorted(protected.custom_fields)
        if obj._custom_field_data.get(key) != _stored_custom_field_value(original["_custom_field_data"], key)
        and not has_action(custom_field_permission_action(key))
    ]
    if custom_field_errors:
        errors[NON_FIELD_ERRORS] = custom_field_errors
    if errors:
        self.validation_error(errors)


def register_field_permission_validators():
    """Register a field permission validator for every model whose `clean()` Nautobot wraps.

    Registration is fixed at startup; which fields are protected is read from `ContentTypeRuleSet` at validation time.
    """
    register_custom_validators(
        [
            build_custom_validator(
                f"{app_label}.{model}", _check_field_permissions, name=f"FieldPermissionValidator_{app_label}_{model}"
            )
            for app_label, models in FeatureQuery("custom_validators").as_dict()
            for model in models
        ]
    )
