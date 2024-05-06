from django.test import TestCase
from django.utils import timezone

from vendors.models import Vendor
from vendors.tests.factories import VendorFactory, HistoricalPerformanceFactory


class VendorModelTestCase(TestCase):
    def setUp(self):
        self.vendor = VendorFactory(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
        )

    def test_vendor_creation(self):
        self.assertEqual(self.vendor.name, "Test Vendor")
        self.assertEqual(self.vendor.contact_details, "Test Contact Details")
        self.assertEqual(self.vendor.address, "Test Address")
        self.assertTrue(self.vendor.vendor_code.startswith("VEN-"))

    def test_add_prefix_to_vendor_code(self):
        self.vendor.vendor_code = "ABC123"
        self.vendor.save()
        self.assertTrue(self.vendor.vendor_code.startswith("VEN-"))

    def test_get_absolute_url(self):
        expected_url = f"/api/vendors/{self.vendor.pk}/"
        self.assertEqual(self.vendor.get_absolute_url(), expected_url)


class HistoricalPerformanceModelTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
        )
        self.historical_performance = HistoricalPerformanceFactory(
            vendor=self.vendor,
            on_time_delivery_rate=90.0,
            quality_rating_avg=8.0,
            average_response_time=2.5,
            fulfillment_rate=95.0,
        )

    def test_historical_performance_creation(self):
        self.assertEqual(self.historical_performance.vendor, self.vendor)
        self.assertEqual(self.historical_performance.on_time_delivery_rate, 90.0)
        self.assertEqual(self.historical_performance.quality_rating_avg, 8.0)
        self.assertEqual(self.historical_performance.average_response_time, 2.5)
        self.assertEqual(self.historical_performance.fulfillment_rate, 95.0)

    def test_historical_performance_str(self):
        expected_str = (
            f"{self.vendor.name} - {self.historical_performance.history_date}"
        )
        self.assertEqual(str(self.historical_performance), expected_str)

    def test_historical_performance_ordering(self):
        # Create another historical performance with a different history date
        historical_performance_2 = HistoricalPerformanceFactory(
            vendor=self.vendor,
            on_time_delivery_rate=95.0,
            quality_rating_avg=9.0,
            average_response_time=2.0,
            fulfillment_rate=97.0,
        )
        historical_performance_2.history_date = timezone.now() - timezone.timedelta(
            days=2
        )
        historical_performance_2.save()

        # Ensure the most recent historical performance is listed first
        self.assertGreater(
            self.historical_performance.history_date,
            historical_performance_2.history_date,
        )
