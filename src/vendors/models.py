from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

from common.models import HasSubModelsMixin

from common.methods import get_unique_code_chars


class Vendor(HasSubModelsMixin):
    vendor_code_prefix = "VEN"

    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
    vendor_code = models.CharField(
        unique=True,
        max_length=16,
        blank=False,
        null=False,
        default=get_unique_code_chars,
        editable=False,
    )

    class Meta:
        verbose_name = _("vendor")
        verbose_name_plural = _("vendors")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.add_prefix_to_vendor_code()
        super().save(*args, **kwargs)

    def add_prefix_to_vendor_code(self):
        """
        Does the actual work to prepend the prefix to the Vendor Code characters when needed. Refactored out
        to be usable outside of the save method.
        """
        prefix = "{}-".format(self.vendor_code_prefix)
        if not self.vendor_code.startswith(prefix):
            self.vendor_code = "{}{}".format(prefix, self.vendor_code)

    def get_absolute_url(self) -> str:
        return reverse(
            "vendors:retrieve-update-destroy-vendors", kwargs={"pk": self.pk}
        )


class HistoricalPerformance(HasSubModelsMixin):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    history_date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.history_date}"

    class Meta:
        ordering = ["-history_date"]
        verbose_name = "Historical Performance"
        verbose_name_plural = "Historical Performances"
