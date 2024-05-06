from django.urls import path
from orders.api.v1 import viewsets

app_name = "orders"

urlpatterns = [
    path("", viewsets.PurchaseOrderListView.as_view(), name="purchase-order-list"),
    path(
        "<int:pk>/",
        viewsets.PurchaseOrderActionView.as_view(),
        name="purchase-order-action",
    ),
    path(
        "<int:pk>/acknowledge",
        viewsets.PurchaseOrderAcknowledgeView.as_view(),
        name="purchase-order-acknowledge",
    ),
]
