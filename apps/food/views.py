from rest_framework import viewsets, permissions, exceptions
from .models import FoodItem, FoodOrder
from .serializers import FoodItemSerializer, FoodOrderSerializer

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAdminUser | ReadOnly]

class FoodOrderViewSet(viewsets.ModelViewSet):
    serializer_class = FoodOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'STAFF']:
            return FoodOrder.objects.all()
        return FoodOrder.objects.filter(booking__user=user)

    def perform_create(self, serializer):
        booking = serializer.validated_data['booking']
        if booking.user != self.request.user:
            raise exceptions.PermissionDenied("You cannot order food for a booking that ensures not belong to you.")
        serializer.save()
