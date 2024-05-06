from copy import deepcopy
from django.test import TestCase

from orders.tests.factories import PurchaseOrderFactory
from vendors.tests.factories import VendorFactory
from orders.tests.mock_data.order import LIST_PO_DATA


class PurchaseOrderTestCase(TestCase):
    def setUp(self):
        # Create a vendor
        self.vendor1 = VendorFactory(
            name="Test Vendor 1",
            contact_details="Test Contact Details 1",
            address="Test Address 1",
        )
        self.vendor2 = VendorFactory(
            name="Test Vendor 2",
            contact_details="Test Contact Details 2",
            address="Test Address 2",
        )

        self.vendor3 = VendorFactory(
            name="Test Vendor 3",
            contact_details="Test Contact Details 3",
            address="Test Address 3",
        )

        self.po_list_data = deepcopy(LIST_PO_DATA)

        # Create some purchase orders
        self.po1 = PurchaseOrderFactory(vendor=self.vendor1, **self.po_list_data[0])
        self.po2 = PurchaseOrderFactory(vendor=self.vendor1, **self.po_list_data[1])
        self.po3 = PurchaseOrderFactory(vendor=self.vendor2, **self.po_list_data[2])
        self.po4 = PurchaseOrderFactory(vendor=self.vendor3, **self.po_list_data[3])
        self.po5 = PurchaseOrderFactory(vendor=self.vendor3, **self.po_list_data[4])
        self.po6 = PurchaseOrderFactory(vendor=self.vendor3, **self.po_list_data[5])

    def test_calc_on_time_delivery_rate(self):
        self.assertEqual(self.po1.calc_on_time_delivery_rate(), 100.00)
        self.assertEqual(self.po2.calc_on_time_delivery_rate(), 100.00)
        self.assertEqual(self.po3.calc_on_time_delivery_rate(), 0.00)
        self.assertEqual(self.po4.calc_on_time_delivery_rate(), 50.00)
        self.assertEqual(self.po5.calc_on_time_delivery_rate(), 50.00)

    def test_calc_avg_quality_ratings(self):
        self.assertEqual(
            self.po1.calc_avg_quality_ratings(), 0.0
        )  # No quality rating provided
        self.assertEqual(
            self.po2.calc_avg_quality_ratings(), 0.0
        )  # No quality rating provided
        self.assertEqual(
            self.po3.calc_avg_quality_ratings(), 0.0
        )  # No completed purchase orders
        self.assertEqual(
            self.po4.calc_avg_quality_ratings(), 0.0
        )  # No quality rating provided

        self.assertEqual(
            self.po5.calc_avg_quality_ratings(), 0.0
        )  # No quality rating provided

        # update quality rating for po1 and po2
        self.po1.quality_rating = 5
        self.po1.save()

        self.po2.quality_rating = 4
        self.po2.save()

        self.assertEqual(self.po1.calc_avg_quality_ratings(), 4.5)
        self.assertEqual(self.po2.calc_avg_quality_ratings(), 4.5)

        # update quality rating for po4 and po5
        self.po4.quality_rating = 5
        self.po4.save()

        self.assertEqual(self.po4.calc_avg_quality_ratings(), 5)

    def test_calc_fulfillment_rate(self):
        self.assertEqual(self.po1.calc_fulfillment_rate(), 100.00)
        self.assertEqual(self.po2.calc_fulfillment_rate(), 100.00)
        self.assertEqual(self.po3.calc_fulfillment_rate(), 0.00)
        self.assertEqual(self.po4.calc_fulfillment_rate(), 66.67)
        self.assertEqual(self.po4.calc_fulfillment_rate(), 66.67)
        self.assertEqual(self.po5.calc_fulfillment_rate(), 66.67)
        self.assertEqual(self.po6.calc_fulfillment_rate(), 66.67)

    def test_calc_avg_response_time(self):
        self.assertEqual(self.po1.calc_avg_response_time(), 36)  # In hours
        self.assertEqual(self.po2.calc_avg_response_time(), 36)  # In hours
        self.assertEqual(
            self.po3.calc_avg_response_time(), 0
        )  # No acknowledged purchase orders

        self.assertEqual(self.po4.calc_avg_response_time(), 36)

        self.assertEqual(self.po5.calc_avg_response_time(), 36)

        self.assertEqual(self.po6.calc_avg_response_time(), 36)
