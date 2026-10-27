"""Models for Granular Field Permissions."""

# Django imports
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Nautobot imports
from nautobot.apps.constants import CHARFIELD_MAX_LENGTH
from nautobot.apps.models import PrimaryModel, extras_features

# If you want to choose a specific model to overload in your class declaration, please reference the following documentation:
# how to chose a database model: https://docs.nautobot.com/projects/core/en/stable/plugins/development/#database-models
# If you want to use the extras_features decorator please reference the following documentation
# https://docs.nautobot.com/projects/core/en/stable/development/core/model-checklist/#extras-features
@extras_features("custom_links", "custom_validators", "export_templates", "graphql", "webhooks")
class GranularFieldPermissionsExampleModel(PrimaryModel):  # pylint: disable=too-many-ancestors
    """Base model for Granular Field Permissions app."""

    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True)
    # additional model fields

    class Meta:
        """Meta class."""

        ordering = ["name"]

        # Option for fixing capitalization (i.e. "Snmp" vs "SNMP")
        # verbose_name = "Granular Field Permissions"

        # Option for fixing plural name (i.e. "Chicken Tenders" vs "Chicken Tendies")
        # verbose_name_plural = "Granular Field Permissionss"

    def __str__(self):
        """Stringify instance."""
        return self.name

class ContentTypeRuleSet(PrimaryModel):
    """Ruleset for a content type"""
    ct = models.OneToOneField(ContentType, on_delete=models.CASCADE, verbose_name="Content Type", unique=True)
    deny_default = models.BooleanField(verbose_name="Deny by default", default=False)


class ContentTypeRule(PrimaryModel):
    """A single rule in a ContentTypeRuleSet"""
    ruleset = models.ForeignKey(to=ContentTypeRuleSet, on_delete=models.CASCADE)
    field = models.CharField(max_length=40)
    groups = models.ManyToManyField(to=Group)
    deny = models.BooleanField(verbose_name="Deny edit")
    allow_create = models.BooleanField(verbose_name="Allow when creating a new object (doesn't apply on a Permit by default ruleset)")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['ruleset', 'field', 'deny'])
        ]