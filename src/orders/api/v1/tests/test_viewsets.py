from copy import deepcopy

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APIClient

from orders.models import PurchaseOrder

from orders.tests.factories import PurchaseOrderFactory
from vendors.tests.factories import VendorFactory


class PurchaseOrderListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.vendor_code = "VEN-pc0e8ktp"

        self.vendor = VendorFactory(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
            vendor_code=self.vendor_code,
        )

        self.url = reverse("orders:purchase-order-list")
        self.data = {
            "order_date": "2024-05-06T12:00:00Z",
            "delivery_date": "2024-05-09T12:00:00Z",
            "items": [
                {
                    "item_no": 10001,
                    "item_name": "Grove Anti - Dandruff",
                    "quantity": 5,
                    "unit_price": 10.0,
                },
                {
                    "item_no": 10002,
                    "item_name": "Shampoo for Hair Growth",
                    "quantity": 15,
                    "unit_price": 10.0,
                },
            ],
            "quantity": 10,
            "vendor": self.vendor.id,
            "quality_rating": 9.5,
        }

        po_sample_data = deepcopy(self.data)
        po_sample_data["vendor"] = self.vendor

        # create purchase order
        self.po1 = PurchaseOrderFactory(**po_sample_data)

    def test_list_purchase_orders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_order(self):
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_purchase_orders_by_vendor_code(self):
        # Filter purchase orders by vendor code
        response = self.client.get(self.url + f"?search={self.vendor_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Expecting only one purchase order with vendor code 'VEN-pc0e8ktp'
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.po1.id)


class PurchaseOrderActionViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.vendor = VendorFactory(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
        )
        self.purchase_order = PurchaseOrderFactory(
            order_date="2024-05-06T12:00:00Z",
            delivery_date="2024-05-09T12:00:00Z",
            items=[
                {
                    "item_no": 10001,
                    "item_name": "Grove Anti - Dandruff",
                    "quantity": 5,
                    "unit_price": 10.0,
                },
                {
                    "item_no": 10002,
                    "item_name": "Shampoo for Hair Growth",
                    "quantity": 15,
                    "unit_price": 10.0,
                },
            ],
            quantity=10,
            vendor=self.vendor,
            quality_rating=9.5,
            status=PurchaseOrder.PENDING,
        )
        self.url = reverse(
            "orders:purchase-order-action", kwargs={"pk": self.purchase_order.pk}
        )
        self.updated_data = {"status": PurchaseOrder.COMPLETED}

    def test_retrieve_purchase_order(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        response = self.client.patch(self.url, self.updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_purchase_order(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PurchaseOrderAcknowledgeViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.vendor = VendorFactory(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
        )
        self.purchase_order = PurchaseOrderFactory(
            order_date="2024-05-06T12:00:00Z",
            delivery_date="2024-05-09T12:00:00Z",
            items=[
                {
                    "item_no": 10001,
                    "item_name": "Grove Anti - Dandruff",
                    "quantity": 5,
                    "unit_price": 10.0,
                },
                {
                    "item_no": 10002,
                    "item_name": "Shampoo for Hair Growth",
                    "quantity": 15,
                    "unit_price": 10.0,
                },
            ],
            quantity=10,
            vendor=self.vendor,
            quality_rating=9.5,
            status=PurchaseOrder.PENDING,
        )
        self.url = reverse(
            "orders:purchase-order-acknowledge", kwargs={"pk": self.purchase_order.pk}
        )
        self.acknowledged_data = {"acknowledgment_date": "2024-05-07T12:00:00Z"}

    def test_acknowledge_purchase_order(self):
        response = self.client.put(self.url, self.acknowledged_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
