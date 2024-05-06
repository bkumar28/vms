import factory

from vendors.models import Vendor, HistoricalPerformance


class VendorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vendor

    name = factory.Faker("company")
    contact_details = factory.Faker("phone_number")
    address = factory.Faker("address")
    on_time_delivery_rate = factory.Faker("random_number", digits=2, fix_len=True)
    quality_rating_avg = factory.Faker("random_number", digits=2, fix_len=True)
    average_response_time = factory.Faker("random_number", digits=2, fix_len=True)
    fulfillment_rate = factory.Faker("random_number", digits=2, fix_len=True)
    vendor_code = factory.Sequence(
        lambda n: f"VEN-{n}"
    )  # Generates a unique vendor code for each instance


class HistoricalPerformanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HistoricalPerformance

    vendor = factory.SubFactory(
        VendorFactory
    )  # Using SubFactory to generate Vendor instances
    history_date = factory.Faker("date_time")
    on_time_delivery_rate = factory.Faker("random_number", digits=2, fix_len=True)
    quality_rating_avg = factory.Faker("random_number", digits=2, fix_len=True)
    average_response_time = factory.Faker("random_number", digits=2, fix_len=True)
    fulfillment_rate = factory.Faker("random_number", digits=2, fix_len=True)
