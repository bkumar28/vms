from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from orders.models import PurchaseOrder
from vendors.models import HistoricalPerformance


@receiver(pre_save, sender=PurchaseOrder)
def track_status_change(sender, instance, **kwargs):
    instance.__original_status = None

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is being created, no need to track status change
        return

    if old_instance.status != instance.status:
        # Status is changing
        instance.__original_status = old_instance.status


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics_on_status_change(sender, instance, created, **kwargs):
    if not created:
        vendor_obj = instance.vendor

        if (
            instance.__original_status is None
            or instance.__original_status == instance.status
        ):
            return

        if instance.status == PurchaseOrder.COMPLETED:
            # Update on-time delivery rate
            on_time_delivery_rate = instance.calc_on_time_delivery_rate()

            # Update quality rating average
            quality_rating_avg = instance.calc_avg_quality_ratings()

            vendor_obj.on_time_delivery_rate = on_time_delivery_rate
            vendor_obj.quality_rating_avg = quality_rating_avg

        # Update fulfillment rate
        fulfillment_rate = instance.calc_fulfillment_rate()
        vendor_obj.fulfillment_rate
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
