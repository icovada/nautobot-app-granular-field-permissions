"""API views for granular_field_permissions."""

from nautobot.apps.api import NautobotModelViewSet

from granular_field_permissions import filters, models
from granular_field_permissions.api import serializers


class ContentTypeRuleSetViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """ContentTypeRuleSet viewset."""

    queryset = models.ContentTypeRuleSet.objects.all()
    serializer_class = serializers.ContentTypeRuleSetSerializer
    filterset_class = filters.ContentTypeRuleSetFilterSet

    # Option for modifying the default HTTP methods:
    # http_method_names = ["get", "post", "put", "patch", "delete", "head", "options", "trace"]
