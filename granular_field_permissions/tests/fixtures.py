"""Create fixtures for tests."""

from granular_field_permissions.models import ContentTypeRuleSet


def create_ContentTypeRuleSet():
    """Fixture to create necessary number of ContentTypeRuleSet for tests."""
    ContentTypeRuleSet.objects.create(name="Test One")
    ContentTypeRuleSet.objects.create(name="Test Two")
    ContentTypeRuleSet.objects.create(name="Test Three")
