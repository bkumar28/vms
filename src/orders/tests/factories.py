from datetime import timedelta
from django.utils import timezone
import factory

from orders.models import PurchaseOrder
from vendors.tests.factories import VendorFactory


class PurchaseOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseOrder

    vendor = factory.SubFactory(VendorFactory)
    order_date = timezone.now()
    delivery_date = timezone.now() + timedelta(days=3)
    items = factory.Faker("pydict", nb_elements=5, variable_nb_elements=True)
    quantity = factory.Faker("random_int", min=1, max=100)
    issue_date = timezone.now()
    acknowledgment_date = timezone.now() + timedelta(days=1)
    quality_rating = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    status = PurchaseOrder.PENDING
