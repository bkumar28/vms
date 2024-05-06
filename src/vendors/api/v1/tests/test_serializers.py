from django.test import TestCase

from vendors.api.v1.serializers import (
    VendorSerializer,
    VendorPerformanceSerializer,
    HistoricalPerformanceSerializer,
)

from vendors.tests.factories import VendorFactory


class VendorSerializerTestCase(TestCase):
    def test_vendor_serializer_valid_data(self):
        vendor_data = {
            "name": "Test Vendor",
            "contact_details": "test@example.com",
            "address": "123 Test Street",
        }
        serializer = VendorSerializer(data=vendor_data)
        self.assertTrue(serializer.is_valid())

    def test_vendor_serializer_invalid_data(self):
        vendor_data = {"name": "", "contact_details": "", "address": ""}
        serializer = VendorSerializer(data=vendor_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 3)


class VendorPerformanceSerializerTestCase(TestCase):
    def test_vendor_performance_serializer_valid_data(self):
        vendor = VendorFactory(
            name="Test Vendor",
            contact_details="test@example.com",
            address="123 Test Street",
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.3,
            fulfillment_rate=98.2,
        )
        serializer = VendorPerformanceSerializer(instance=vendor)
        self.assertEqual(serializer.data["on_time_delivery_rate"], 95.5)
        self.assertEqual(serializer.data["quality_rating_avg"], 4.5)
        self.assertEqual(serializer.data["average_response_time"], 2.3)
        self.assertEqual(serializer.data["fulfillment_rate"], 98.2)


class HistoricalPerformanceSerializerTestCase(TestCase):
    def test_historical_performance_serializer_valid_data(self):
        vendor = VendorFactory(
            name="Test Vendor",
            contact_details="test@example.com",
            address="123 Test Street",
        )
        historical_performance_data = {
            "vendor": vendor.id,
            "on_time_delivery_rate": 95.5,
            "quality_rating_avg": 4.5,
            "average_response_time": 2.3,
            "fulfillment_rate": 98.2,
        }
        serializer = HistoricalPerformanceSerializer(data=historical_performance_data)
        self.assertTrue(serializer.is_valid())
