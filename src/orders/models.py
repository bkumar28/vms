from django.db import models
from django.urls import reverse

from common.models import HasSubModelsMixin
from common.methods import get_unique_code_chars


class PurchaseOrder(HasSubModelsMixin):
    po_number_prefix = "PO"

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = (
        (PENDING, "pending"),
        (COMPLETED, "completed"),
        (CANCELLED, "cancelled"),
    )

    po_number = models.CharField(
        unique=True,
        max_length=16,
        blank=False,
        null=False,
        default=get_unique_code_chars,
        editable=False,
    )

    vendor = models.ForeignKey(
        "vendors.Vendor", on_delete=models.CASCADE, related_name="purchase_orders"
    )
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    quality_rating = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)

    # We will utilize this class variable to systematically track the status of each purchase order
    # within our signal implementation. Leveraging this data, we can accurately calculate
    # performance metrics tailored to our specific needs.
    __original_status = None

    class Meta:
        ordering = ["-order_date"]
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"

    def __str__(self):
        return f"{self.po_number} - {self.vendor.name}"

    def get_absolute_url(self) -> str:
        return reverse("orders:purchase-order-actions", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        self.add_prefix_to_po_number()
        super().save(*args, **kwargs)

    def add_prefix_to_po_number(self):
        """
        Does the actual work to prepend the prefix to the Purchase Orders Number
          characters when needed. Refactored out to be usable outside of the save method.
        """
        prefix = "{}-".format(self.po_number_prefix)
        if not self.po_number.startswith(prefix):
            self.po_number = "{}{}".format(prefix, self.po_number)

    def get_purchase_orders_by_status(self, status: str) -> models.QuerySet:
        """
        Filter vendor purchase orders by status
        """
        if status in [self.COMPLETED, self.CANCELLED, self.PENDING]:
            return PurchaseOrder.objects.filter(status=status, vendor=self.vendor)
        else:
            return None

    def calc_on_time_delivery_rate(self) -> float:
        """
        The function calculates the on-time delivery rate by dividing the count of purchase orders
        fulfilled on or before their delivery dates by the total count of purchase orders.
        """
        total_completed_purchases = self.get_purchase_orders_by_status(
            status=self.COMPLETED
        )

        completed_purchases = total_completed_purchases.filter(
            acknowledgment_date__lte=models.F("delivery_date")
        )

        try:
            delivery_rate = (
                completed_purchases.count() / total_completed_purchases.count()
            ) * 100
            return round(delivery_rate, 2) if delivery_rate else 0
        except ZeroDivisionError:
            return 0

    def calc_avg_quality_ratings(self) -> float:
        """
        The function calculates the average quality rating of completed purchase orders.
        """
        total_completed_purchases = self.get_purchase_orders_by_status(
            status=self.COMPLETED
        ).exclude(quality_rating__isnull=True)

        quality_rating_avg = total_completed_purchases.aggregate(
            models.Avg("quality_rating")
        )["quality_rating__avg"]

        quality_rating_avg = round(quality_rating_avg, 2) if quality_rating_avg else 0

        return quality_rating_avg

    def calc_fulfillment_rate(self) -> float:
        """
        The function calculates the fulfillment rate by dividing the number of completed
        purchase orders by the total number of purchase orders.
        """
        # get all vendor purchase orders
        total_purchases = PurchaseOrder.objects.filter(vendor=self.vendor)

        # Counting the number of successfully fulfilled POs (status 'completed' without issues)
        fulfilled_purchases = total_purchases.filter(
            status=PurchaseOrder.COMPLETED, issue_date__isnull=False
        )

        try:
            fulfillment_rate = (
                fulfilled_purchases.count() / total_purchases.count()
            ) * 100
        except ZeroDivisionError:
            return 0

        # Rounding the fulfillment rate to two decimal places
        fulfillment_rate = round(fulfillment_rate, 2)

        return fulfillment_rate

    def calc_avg_response_time(self) -> float:
        """
        The function calculates the average response time for purchase orders
        that have both an issue date and an acknowledgment date.
        """
        # Compute the time difference between issue_date and acknowledgment_date for each PO
        time_difference_expression = models.ExpressionWrapper(
            models.F("acknowledgment_date") - models.F("issue_date"),
            output_field=models.fields.DurationField(),
        )

        # Filter purchase orders for the vendor
        purchase_orders = PurchaseOrder.objects.filter(vendor=self.vendor)

        # Exclude purchase orders where either issue_date or acknowledgment_date is None
        purchase_orders = purchase_orders.exclude(issue_date__isnull=True).exclude(
            acknowledgment_date__isnull=True
        )

        # Aggregate the average of time differences for all POs of the vendor
        average_response_time = purchase_orders.aggregate(
            avg_time_difference=models.Avg(time_difference_expression)
        )["avg_time_difference"]

        # convert average response total seconds into hours
        average_response_time = round(
            (
                average_response_time.total_seconds() / 3600
                if average_response_time
                else 0.0
            ),
            2,
        )

        return average_response_time
