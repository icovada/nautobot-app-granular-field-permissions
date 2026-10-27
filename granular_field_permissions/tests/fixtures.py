"""Create fixtures for tests."""

from granular_field_permissions.models import GranularFieldPermissionsExampleModel


def create_granularfieldpermissionsexamplemodel():
    """Fixture to create necessary number of GranularFieldPermissionsExampleModel for tests."""
    GranularFieldPermissionsExampleModel.objects.create(name="Test One")
    GranularFieldPermissionsExampleModel.objects.create(name="Test Two")
    GranularFieldPermissionsExampleModel.objects.create(name="Test Three")
