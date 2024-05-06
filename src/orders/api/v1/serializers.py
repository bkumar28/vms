from django.utils.translation import gettext as _
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import ValidationError


from orders.models import PurchaseOrder
from orders import signals


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        exclude = ["created_at", "updated_at"]
        extra_kwargs = {
            "order_date": {
                "error_messages": {"required": _("please enter valid order date.")}
            },
            "delivery_date": {
                "error_messages": {"required": _("please enter valid delivery date.")}
            },
            "quantity": {
                "error_messages": {
                    "required": _("please enter valid total item quantity.")
                }
            },
            "vendor": {
                "error_messages": {"required": _("please enter valid vendor Id.")}
            },
        }

    def validate_quality_rating(self, value):
        if value and (value < 0 or value > 10):
            raise ValidationError(
                "Please enter valid quality ratings number between 0 to 10"
            )
        return value


class PurchaseOrderAcknowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["acknowledgment_date"]
        extra_kwargs = {"acknowledgment_date": {"required": True}}

    def validate_acknowledgment_date(self, value):
        if not value:
            raise ValidationError("Please enter valid acknowledgment date.")
        return value
