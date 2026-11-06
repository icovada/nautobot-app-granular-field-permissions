"""Django admin for granular_field_permissions."""

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from nautobot.apps.admin import NautobotModelAdmin

from granular_field_permissions.models import (
    ContentTypeRuleSet,
    protectable_custom_field_keys,
    protectable_field_names,
)


class ContentTypeRuleSetForm(forms.ModelForm):
    """Ruleset form offering a choice of protectable fields and custom fields once the content type is known."""

    class Meta:
        """Meta attributes."""

        model = ContentTypeRuleSet
        fields = ["content_type", "protected_fields", "protected_custom_fields"]
        help_texts = {
            "protected_fields": "Comma-separated field names. Once saved, the ruleset offers a list to pick from.",
            "protected_custom_fields": "Comma-separated custom field keys. Once saved, the ruleset offers a list "
            "to pick from.",
        }

    def __init__(self, *args, **kwargs):
        """Replace the free-text lists with a choice of protectable fields and custom fields when editing."""
        super().__init__(*args, **kwargs)
        if self.instance.content_type_id is None:
            return
        model_class = self.instance.content_type.model_class()
        self.fields["protected_fields"] = forms.MultipleChoiceField(
            choices=[(name, name) for name in protectable_field_names(model_class)],
            widget=FilteredSelectMultiple("fields", is_stacked=False),
            required=False,
        )
        self.fields["protected_custom_fields"] = forms.MultipleChoiceField(
            choices=[(key, key) for key in protectable_custom_field_keys(model_class)],
            widget=FilteredSelectMultiple("custom fields", is_stacked=False),
            required=False,
        )


@admin.register(ContentTypeRuleSet)
class ContentTypeRuleSetAdmin(NautobotModelAdmin):
    """Admin for ContentTypeRuleSet."""

    form = ContentTypeRuleSetForm
    list_display = ["content_type", "protected_field_list", "protected_custom_field_list"]

    @admin.display(description="Protected fields")
    def protected_field_list(self, obj):
        """Render protected fields as a comma-separated list."""
        return ", ".join(obj.protected_fields)

    @admin.display(description="Protected custom fields")
    def protected_custom_field_list(self, obj):
        """Render protected custom fields as a comma-separated list."""
        return ", ".join(obj.protected_custom_fields)

    def get_readonly_fields(self, request, obj=None):
        """Lock the content type once created, so the offered fields always belong to the ruleset's model."""
        if obj is not None:
            return ["content_type"]
        return []
