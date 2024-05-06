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
            "status": PurchaseOrder.COMPLETED,
        }
        self.serializer = PurchaseOrderSerializer(data=self.data)

    def test_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_quality_rating(self):
        data = deepcopy(self.data)
        data["quality_rating"] = 11  # Quality rating out of range
        serializer = PurchaseOrderSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


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
