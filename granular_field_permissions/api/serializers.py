"""API serializers for granular_field_permissions."""

from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin

from granular_field_permissions import models


class GranularFieldPermissionsExampleModelSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """GranularFieldPermissionsExampleModel Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.GranularFieldPermissionsExampleModel
        fields = "__all__"

        # Option for disabling write for certain fields:
        # read_only_fields = []
