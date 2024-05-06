from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import PurchaseOrder
from vendors.models import HistoricalPerformance


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics_on_status_change(sender, instance, created, **kwargs):
    vendor_obj = instance.vendor
    update_vendor = False

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if old_instance.status != instance.status and instance.status == instance.COMPLETED:
        vendor = instance.vendor
        # Update on-time delivery rate
        on_time_delivery_rate = instance.calc_on_time_delivery_rate()

        # Update quality rating average
        quality_rating_avg = instance.calc_avg_quality_ratings()

        vendor_obj.on_time_delivery_rate = on_time_delivery_rate
        vendor_obj.quality_rating_avg = quality_rating_avg
        vendor_obj.fulfillment_rate = fulfillment_rate

        update_vendor = True

    if old_instance.status != instance.status:
        # Update fulfillment rate
        fulfillment_rate = instance.calc_fulfillment_rate()
        vendor_obj.fulfillment_rate

        update_vendor = True

    if update_vendor:
        vendor_obj.save()

        # create performance history
        HistoricalPerformance.objects.create(
            vendor=vendor_obj,
            on_time_delivery_rate=vendor_obj.on_time_delivery_rate,
            quality_rating_avg=vendor_obj.quality_rating_avg,
            fulfillment_rate=vendor_obj.fulfillment_rate,
            average_response_time=vendor_obj.average_response_time,
        )


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics_on_acknowledgment(sender, instance, created, **kwargs):
    if instance.acknowledgment_date:
        vendor = instance.vendor
        # Update average response time
        avg_response_time = instance.calc_avg_response_time()
        vendor.avg_response_time = avg_response_time
        vendor.save()
