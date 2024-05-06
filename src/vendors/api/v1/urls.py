from django.urls import path
from vendors.api.v1 import viewsets

app_name = "vendors"

urlpatterns = [
    path("", viewsets.VendorListView.as_view(), name="list-create-vendors"),
    path(
        "<int:pk>/",
        viewsets.VendorActionView.as_view(),
        name="retrieve-update-destroy-vendors",
    ),
    path(
        "<int:pk>/performance/",
        viewsets.VendorPerformanceView.as_view(),
        name="retrieve-vendor-performance",
    ),
    path(
        "<int:pk>/performance/history",
        viewsets.VendorPerformanceHistoryView.as_view(),
        name="list-vendor-performance-history",
    ),
]
