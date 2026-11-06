"""Test ContentTypeRuleSet Filter."""

from nautobot.apps.testing import FilterTestCases

from granular_field_permissions import filters, models
from granular_field_permissions.tests import fixtures


class ContentTypeRuleSetFilterTestCase(FilterTestCases.FilterTestCase):  # pylint: disable=too-many-ancestors
    """ContentTypeRuleSet Filter Test Case."""

    queryset = models.ContentTypeRuleSet.objects.all()
    filterset = filters.ContentTypeRuleSetFilterSet
    generic_filter_tests = (
        ("id",),
        ("created",),
        ("last_updated",),
        ("name",),
    )

    @classmethod
    def setUpTestData(cls):
        """Setup test data for ContentTypeRuleSet Model."""
        fixtures.create_ContentTypeRuleSet()

    def test_q_search_name(self):
        """Test using Q search with name of ContentTypeRuleSet."""
        params = {"q": "Test One"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_invalid(self):
        """Test using invalid Q search for ContentTypeRuleSet."""
        params = {"q": "test-five"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)
