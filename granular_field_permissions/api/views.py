"""API views for granular_field_permissions."""

from nautobot.apps.api import NautobotModelViewSet

from granular_field_permissions import filters, models
from granular_field_permissions.api import serializers


class GranularFieldPermissionsExampleModelViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """GranularFieldPermissionsExampleModel viewset."""

    queryset = models.GranularFieldPermissionsExampleModel.objects.all()
    serializer_class = serializers.GranularFieldPermissionsExampleModelSerializer
    filterset_class = filters.GranularFieldPermissionsExampleModelFilterSet

    # Option for modifying the default HTTP methods:
    # http_method_names = ["get", "post", "put", "patch", "delete", "head", "options", "trace"]
