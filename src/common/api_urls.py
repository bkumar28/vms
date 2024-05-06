from django.urls import path, include

urlpatterns = [
    path(r"vendors/", include("vendors.api.v1.urls")),
    path(r"purchase_orders/", include("orders.api.v1.urls")),
]
