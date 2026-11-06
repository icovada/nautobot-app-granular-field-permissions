"""Models for Granular Field Permissions."""

# Django imports
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db import models

# Nautobot imports
from nautobot.apps.constants import CHARFIELD_MAX_LENGTH
from nautobot.apps.models import JSONArrayField, PrimaryModel, extras_features
from nautobot.apps.utils import FeatureQuery
from nautobot.extras.models import CustomField
from nautobot.users.models import ObjectPermission

FIELD_PERMISSION_ACTION_PREFIX = "field_"
CUSTOM_FIELD_PERMISSION_ACTION_PREFIX = "cf_"


def field_permission_action(field_name):
    """Return the `ObjectPermission` action granting edit access to `field_name`, e.g. `field_name`."""
    return f"{FIELD_PERMISSION_ACTION_PREFIX}{field_name}"


def custom_field_permission_action(key):
    """Return the `ObjectPermission` action granting edit access to custom field `key`, e.g. `cf_foo`."""
    return f"{CUSTOM_FIELD_PERMISSION_ACTION_PREFIX}{key}"


def _action_length_error(name, action):
    """Return why `action` can't be stored in an `ObjectPermission`, or `None` if it fits."""
    max_action_length = ObjectPermission._meta.get_field("actions").base_field.max_length
    if len(action) > max_action_length:
        return (
            f"'{name}' is too long: the action '{action}' exceeds "
            f"the {max_action_length} characters allowed in an ObjectPermission."
        )
    return None


def protected_field_error(model_class, field_name):
    """Return why `field_name` of `model_class` can't be protected, or `None` if it can."""
    try:
        model_field = model_class._meta.get_field(field_name)
    except FieldDoesNotExist:
        return f"{model_class._meta.label} has no field named '{field_name}'."
    if field_name == "_custom_field_data":
        # Not a form field, so an error keyed to it would make Django's ModelForm raise ValueError.
        return "Custom fields are protected individually, through the protected custom fields."
    if model_field.auto_created or not getattr(model_field, "editable", False):
        return f"'{field_name}' is not an editable field of {model_class._meta.label}."
    if model_field.many_to_many:
        # M2M values are saved after `clean()` runs, so changes to them can't be detected.
        return f"'{field_name}' is a many-to-many field and can't be protected."
    return _action_length_error(field_name, field_permission_action(field_name))


def protectable_field_names(model_class):
    """Return the names of all fields of `model_class` that can be protected."""
    return [
        field.name for field in model_class._meta.get_fields() if protected_field_error(model_class, field.name) is None
    ]


def protected_custom_field_error(model_class, key):
    """Return why custom field `key` of `model_class` can't be protected, or `None` if it can."""
    if not CustomField.objects.get_for_model(model_class).filter(key=key).exists():
        return f"{model_class._meta.label} has no custom field with key '{key}'."
    return _action_length_error(key, custom_field_permission_action(key))


def protectable_custom_field_keys(model_class):
    """Return the keys of all custom fields of `model_class` that can be protected."""
    return [
        custom_field.key
        for custom_field in CustomField.objects.get_for_model(model_class)
        if _action_length_error(custom_field.key, custom_field_permission_action(custom_field.key)) is None
    ]


class ContentTypeRuleSet(PrimaryModel):
    """Fields and custom fields of a content type that may only be changed by users granted the matching action.

    Edit access is granted through a regular `ObjectPermission` on the same content type, with the action returned
    by `field_permission_action()` or `custom_field_permission_action()`, so it supports users, groups and
    constraints like any other permission.
    """

    # Only models with the `custom_validators` feature get their `clean()` wrapped by Nautobot at startup,
    # so rulesets on any other model would never be enforced.
    content_type = models.OneToOneField(
        to=ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=FeatureQuery("custom_validators"),
        verbose_name="Content Type",
    )
    protected_fields = JSONArrayField(
        base_field=models.CharField(max_length=CHARFIELD_MAX_LENGTH), blank=True, default=list
    )
    protected_custom_fields = JSONArrayField(
        base_field=models.CharField(max_length=CHARFIELD_MAX_LENGTH), blank=True, default=list
    )

    def clean(self):
        """Ensure every protected field and custom field exists on the model and fits in an `ObjectPermission` action."""
        super().clean()

        if self.content_type_id is None:
            return
        model_class = self.content_type.model_class()
        errors = {}
        field_errors = [
            error
            for field_name in self.protected_fields
            if (error := protected_field_error(model_class, field_name)) is not None
        ]
        if field_errors:
            errors["protected_fields"] = field_errors
        custom_field_errors = [
            error
            for key in self.protected_custom_fields
            if (error := protected_custom_field_error(model_class, key)) is not None
        ]
        if custom_field_errors:
            errors["protected_custom_fields"] = custom_field_errors
        if errors:
            raise ValidationError(errors)