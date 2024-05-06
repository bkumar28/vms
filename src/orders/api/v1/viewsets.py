from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters

from orders.models import PurchaseOrder

from orders.api.v1.serializers import (
    PurchaseOrderSerializer,
    PurchaseOrderAcknowledgeSerializer,
)


class PurchaseOrderListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["vendor__vendor_code"]  # Filter by vendor code


class PurchaseOrderActionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderAcknowledgeView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderAcknowledgeSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid()
        self.perform_update(serializer=serializer)
        return Response(
            {
                "status": "success",
                "message": "Purchase order has been acknowledged successfully.",
                "code": "success_acknowledgement",
            },
            status=status.HTTP_200_OK,
        )
