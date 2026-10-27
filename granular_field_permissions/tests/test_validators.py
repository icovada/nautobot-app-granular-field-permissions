"""Test runtime-generated CustomValidators."""

from django.core.exceptions import ValidationError
from nautobot.apps.testing import TestCase
from nautobot.dcim.models import Manufacturer


class TestRuntimeManufacturerValidator(TestCase):
    """Test the Manufacturer validator registered at app startup."""

    def test_manufacturer_name_validation(self):
        """Manufacturer names starting with a lowercase letter are rejected."""
        for name, valid in (("Acme", True), ("acme", False)):
            with self.subTest(name=name):
                manufacturer = Manufacturer(name=name)
                if valid:
                    manufacturer.validated_save()
                else:
                    with self.assertRaises(ValidationError) as context:
                        manufacturer.validated_save()
                    self.assertIn("name", context.exception.message_dict)
