"""API serializers for granular_field_permissions."""

from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin

from granular_field_permissions import models


class ContentTypeRuleSetSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """ContentTypeRuleSet Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ContentTypeRuleSet
        fields = "__all__"

        # Option for disabling write for certain fields:
        # read_only_fields = []
