"""Test GranularFieldPermissionsExampleModel Filter."""

from nautobot.apps.testing import FilterTestCases

from granular_field_permissions import filters, models
from granular_field_permissions.tests import fixtures


class GranularFieldPermissionsExampleModelFilterTestCase(FilterTestCases.FilterTestCase):  # pylint: disable=too-many-ancestors
    """GranularFieldPermissionsExampleModel Filter Test Case."""

    queryset = models.GranularFieldPermissionsExampleModel.objects.all()
    filterset = filters.GranularFieldPermissionsExampleModelFilterSet
    generic_filter_tests = (
        ("id",),
        ("created",),
        ("last_updated",),
        ("name",),
    )

    @classmethod
    def setUpTestData(cls):
        """Setup test data for GranularFieldPermissionsExampleModel Model."""
        fixtures.create_granularfieldpermissionsexamplemodel()

    def test_q_search_name(self):
        """Test using Q search with name of GranularFieldPermissionsExampleModel."""
        params = {"q": "Test One"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_invalid(self):
        """Test using invalid Q search for GranularFieldPermissionsExampleModel."""
        params = {"q": "test-five"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)
