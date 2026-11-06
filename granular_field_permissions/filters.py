"""Filtering for granular_field_permissions."""

from nautobot.apps.filters import NameSearchFilterSet, NautobotFilterSet

from granular_field_permissions import models


class ContentTypeRuleSetFilterSet(NameSearchFilterSet, NautobotFilterSet):  # pylint: disable=too-many-ancestors
    """Filter for ContentTypeRuleSet."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ContentTypeRuleSet

        # add any fields from the model that you would like to filter your searches by using those
        fields = "__all__"
