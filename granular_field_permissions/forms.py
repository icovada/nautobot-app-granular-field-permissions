"""Forms for granular_field_permissions."""

from django import forms
from nautobot.apps.constants import CHARFIELD_MAX_LENGTH
from nautobot.apps.forms import NautobotBulkEditForm, NautobotFilterForm, NautobotModelForm, TagsBulkEditFormMixin

from granular_field_permissions import models


class GranularFieldPermissionsExampleModelForm(NautobotModelForm):  # pylint: disable=too-many-ancestors
    """GranularFieldPermissionsExampleModel creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.GranularFieldPermissionsExampleModel
        fields = "__all__"


class GranularFieldPermissionsExampleModelBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):  # pylint: disable=too-many-ancestors
    """GranularFieldPermissionsExampleModel bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.GranularFieldPermissionsExampleModel.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False, max_length=CHARFIELD_MAX_LENGTH)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class GranularFieldPermissionsExampleModelFilterForm(NautobotFilterForm):  # pylint: disable=too-many-ancestors
    """Filter form to filter searches."""

    model = models.GranularFieldPermissionsExampleModel
    field_order = ["q", "name"]

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name.",
    )
    name = forms.CharField(required=False, label="Name")
