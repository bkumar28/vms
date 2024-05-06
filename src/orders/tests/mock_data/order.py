from orders.models import PurchaseOrder
from datetime import timedelta
from django.utils import timezone

SINGLE_PO_DATA = {
    "order_date": timezone.now(),
    "delivery_date": timezone.now() + timedelta(days=3),
    "items": [
        {
            "item_no": 10001,
            "item_name": "Grove Anti - Dandruff",
            "quantity": 5,
            "unit_price": 10.0,
        },
        {
            "item_no": 10002,
            "item_name": "Shampoo for Hair Growth",
            "quantity": 15,
            "unit_price": 10.0,
        },
    ],
    "quantity": 5,
    "quality_rating": None,
    "issue_date": None,
    "acknowledgment_date": timezone.now() + timedelta(days=2),
}

LIST_PO_DATA = [
    {
        "order_date": timezone.now(),
        "delivery_date": timezone.now() + timedelta(days=3),
        "items": [
            {
                "item_no": 10001,
                "item_name": "Grove Anti - Dandruff",
                "quantity": 5,
                "unit_price": 10.0,
            },
            {
                "item_no": 10002,
                "item_name": "Shampoo for Hair Growth",
                "quantity": 15,
                "unit_price": 10.0,
            },
        ],
        "quantity": 5,
        "quality_rating": None,
        "issue_date": timezone.now(),
        "acknowledgment_date": timezone.now() + timedelta(days=2),
        "status": PurchaseOrder.COMPLETED,
    },
    {
        "order_date": timezone.now(),
        "delivery_date": timezone.now() + timedelta(days=5),
        "items": [
            {
                "item_no": 10001,
                "item_name": "Grove Anti - Dandruff",
                "quantity": 5,
                "unit_price": 10.0,
            },
            {
                "item_no": 10002,
                "item_name": "Shampoo for Hair Growth",
                "quantity": 15,
                "unit_price": 10.0,
            },
        ],
        "quantity": 5,
        "quality_rating": None,
        "issue_date": timezone.now(),
        "acknowledgment_date": timezone.now() + timedelta(days=1),
        "status": PurchaseOrder.COMPLETED,
    },
    {
        "order_date": timezone.now(),
        "delivery_date": timezone.now() + timedelta(days=7),
        "items": [
            {
                "item_no": 10001,
                "item_name": "Grove Anti - Dandruff",
                "quantity": 5,
                "unit_price": 10.0,
            },
            {
                "item_no": 10002,
                "item_name": "Shampoo for Hair Growth",
                "quantity": 15,
                "unit_price": 10.0,
            },
        ],
        "quantity": 5,
        "quality_rating": None,
        "issue_date": None,
        "acknowledgment_date": None,
        "status": PurchaseOrder.PENDING,
    },
    {
        "order_date": timezone.now(),
        "delivery_date": timezone.now() + timedelta(days=2),
        "items": [
            {
                "item_no": 10001,
                "item_name": "Grove Anti - Dandruff",
                "quantity": 5,
                "unit_price": 10.0,
            },
            {
                "item_no": 10002,
                "item_name": "Shampoo for Hair Growth",
                "quantity": 15,
                "unit_price": 10.0,
            },
        ],
        "quantity": 5,
        "quality_rating": None,
        "issue_date": timezone.now(),
        "acknowledgment_date": timezone.now(),
        "status": PurchaseOrder.COMPLETED,
    },
    {
        "order_date": timezone.now(),
        "delivery_date": timezone.now() + timedelta(days=2),
        "items": [
            {
                "item_no": 10001,
                "item_name": "Grove Anti - Dandruff",
                "quantity": 5,
                "unit_price": 10.0,
            },
            {
                "item_no": 10002,
                "item_name": "Shampoo for Hair Growth",
                "quantity": 15,
                "unit_price": 10.0,
            },
        ],
        "quantity": 5,
        "quality_rating": None,
        "issue_date": timezone.now(),
        "acknowledgment_date": timezone.now() + timedelta(days=3),
        "status": PurchaseOrder.COMPLETED,
    },
    {
        "order_date": timezone.now(),
        "delivery_date": timezone.now() + timedelta(days=2),
        "items": [
            {
                "item_no": 10001,
                "item_name": "Grove Anti - Dandruff",
                "quantity": 5,
                "unit_price": 10.0,
            },
            {
                "item_no": 10002,
                "item_name": "Shampoo for Hair Growth",
                "quantity": 15,
                "unit_price": 10.0,
            },
        ],
        "quantity": 5,
        "quality_rating": None,
        "issue_date": None,
        "acknowledgment_date": None,
        "status": PurchaseOrder.CANCELLED,
    },
]
