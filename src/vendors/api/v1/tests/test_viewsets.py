from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from vendors.models import Vendor

from vendors.tests.factories import VendorFactory, HistoricalPerformanceFactory


class VendorListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.url = reverse("vendors:list-create-vendors")
        self.vendor_data = {
            "name": "Test Vendor",
            "contact_details": "test@example.com",
            "address": "123 Test Street",
        }

    def test_create_vendor(self):
        response = self.client.post(self.url, self.vendor_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, "Test Vendor")

    def test_list_vendors(self):
        vendor = VendorFactory(**self.vendor_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], vendor.name)


class VendorActionViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.vendor = VendorFactory(
            name="Test Vendor",
            contact_details="test@example.com",
            address="123 Test Street",
        )
        self.url = reverse(
            "vendors:retrieve-update-destroy-vendors", kwargs={"pk": self.vendor.pk}
        )
        self.update_data = {
            "name": "Updated Vendor Name",
            "contact_details": "updated@example.com",
            "address": "456 Updated Street",
        }

    def test_retrieve_vendor(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.vendor.name)

    def test_update_vendor(self):
        response = self.client.put(self.url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, "Updated Vendor Name")

    def test_delete_vendor(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vendor.objects.filter(pk=self.vendor.pk).exists())


class VendorPerformanceViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.vendor = VendorFactory(
            name="Test Vendor",
            contact_details="test@example.com",
            address="123 Test Street",
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.3,
            fulfillment_rate=98.2,
        )
        self.url = reverse(
            "vendors:retrieve-vendor-performance", kwargs={"pk": self.vendor.pk}
        )

    def test_retrieve_vendor_performance(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["on_time_delivery_rate"], 95.5)


class VendorPerformanceHistoryViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.vendor = VendorFactory(
            name="Test Vendor",
            contact_details="test@example.com",
            address="123 Test Street",
        )
        self.historical_performance = HistoricalPerformanceFactory(
            vendor=self.vendor,
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.3,
            fulfillment_rate=98.2,
        )
        self.url = reverse(
            "vendors:list-vendor-performance-history", kwargs={"pk": self.vendor.pk}
        )

    def test_list_vendor_performance_history(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["on_time_delivery_rate"], 95.5)
