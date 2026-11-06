"""App declaration for granular_field_permissions."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class GranularFieldPermissionsConfig(NautobotAppConfig):
    """App configuration for the granular_field_permissions app."""

    name = "granular_field_permissions"
    verbose_name = "Granular Field Permissions"
    version = __version__
    author = "Network to Code, LLC"
    description = "Granular Field Permissions."
    base_url = "granular-field-permissions"
    required_settings = []
    default_settings = {}
    docs_view_name = "plugins:granular_field_permissions:docs"
    searchable_models = ["ContentTypeRuleSet"]

    def ready(self):
        """Register field permission validators and their cache invalidation signals."""
        super().ready()

        from granular_field_permissions.validators import (  # pylint: disable=import-outside-toplevel
            register_field_permission_validators,
        )

        # Deferred: this module is imported before Django's app registry is populated, and `validators`
        # imports this app's models.
        register_field_permission_validators()


config = GranularFieldPermissionsConfig  # pylint:disable=invalid-name
