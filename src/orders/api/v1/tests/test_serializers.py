from copy import deepcopy
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from orders.models import PurchaseOrder

from orders.api.v1.serializers import (
    PurchaseOrderSerializer,
    PurchaseOrderAcknowledgeSerializer,
)

from orders.tests.factories import PurchaseOrderFactory
from vendors.tests.factories import VendorFactory


class PurchaseOrderSerializerTestCase(TestCase):
    def setUp(self):
        self.vendor = VendorFactory(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
        )

        self.data = {
            "order_date": timezone.now(),
            "delivery_date": timezone.now() + timezone.timedelta(days=3),
            "items": {"item1": "description1", "item2": "description2"},
            "quantity": 10,
            "vendor": self.vendor.id,
            "quality_rating": 9.5,
        }

        self.purchase_order1 = PurchaseOrderFactory(
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=7),
            quantity=100,
            vendor=self.vendor,
            items={"item1": "description1", "item2": "description2"},
        )

        self.purchase_order2 = PurchaseOrderFactory(
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=5),
            quantity=10,
            vendor=self.vendor,
            items={"item1": "description1", "item2": "description2"},
        )

    def test_valid_data(self):
        self.serializer = PurchaseOrderSerializer(data=self.data)
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_quality_rating(self):
        data = self.data
        data["quality_rating"] = 11  # Quality rating out of range
        serializer = PurchaseOrderSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create_purchase_order(self):
        data = {
            "order_date": timezone.now(),
            "delivery_date": timezone.now() + timezone.timedelta(days=3),
            "items": {"item1": "description1", "item2": "description2"},
            "quantity": 10,
            "vendor": self.vendor.id,
        }
        serializer = PurchaseOrderSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        purchase_order = serializer.save()

        # Check that the purchase order was created successfully
        self.assertIsNotNone(purchase_order.id)

    def test_update_purchase_order(self):
        data = {
            "order_date": timezone.now() - timezone.timedelta(days=1),
            "delivery_date": timezone.now() + timezone.timedelta(days=3),
            "quantity": 150,
            "status": PurchaseOrder.COMPLETED,
        }

        serializer = PurchaseOrderSerializer(
            instance=self.purchase_order1, data=data, partial=True
        )
        self.assertTrue(serializer.is_valid())
        updated_purchase_order = serializer.save()

        # Check that the purchase order was updated successfully
        self.assertEqual(updated_purchase_order.order_date, data["order_date"])
        self.assertEqual(updated_purchase_order.delivery_date, data["delivery_date"])
        self.assertEqual(updated_purchase_order.quantity, data["quantity"])
        self.assertEqual(updated_purchase_order.status, PurchaseOrder.COMPLETED)

    def test_cancel_purchase_order(self):
        data = {"status": PurchaseOrder.CANCELLED}

        serializer = PurchaseOrderSerializer(
            instance=self.purchase_order2, data=data, partial=True
        )
        self.assertTrue(serializer.is_valid())
        updated_purchase_order = serializer.save()

        # Check that the purchase order was updated successfully
        self.assertEqual(updated_purchase_order.status, PurchaseOrder.CANCELLED)


class PurchaseOrderAcknowledgeSerializerTestCase(TestCase):
    def setUp(self):
        self.vendor = VendorFactory(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
        )

        self.purchase_order = PurchaseOrderFactory(
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=3),
            items={"item1": "description1", "item2": "description2"},
            quantity=10,
            vendor=self.vendor,
            quality_rating=9.5,
            status=PurchaseOrder.PENDING,
        )
        self.data = {"acknowledgment_date": timezone.now()}
        self.serializer = PurchaseOrderAcknowledgeSerializer(
            instance=self.purchase_order, data=self.data
        )

    def test_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_acknowledgment_date(self):
        self.data["acknowledgment_date"] = None
        serializer = PurchaseOrderAcknowledgeSerializer(
            instance=self.purchase_order, data=self.data
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
