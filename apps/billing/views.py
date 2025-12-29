from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer
from apps.bookings.models import Booking
from apps.events.models import Event

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.role == 'STAFF':
            return Invoice.objects.all()
        return Invoice.objects.filter(user=user)

    @action(detail=False, methods=['post'])
    def generate_booking_invoice(self, request):
        booking_id = request.data.get('booking_id')
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role != 'ADMIN' and request.user.role != 'STAFF' and booking.user != request.user:
             return Response({'error': 'You cannot generate invoice for this booking'}, status=status.HTTP_403_FORBIDDEN)

        # Calculate total
        days = (booking.check_out_date - booking.check_in_date).days
        room_cost = booking.room.room_type.price_per_night * days
        
        food_cost = 0
        for order in booking.food_orders.all():
            for item in order.items.all():
                food_cost += item.food_item.price * item.quantity
        
        total_amount = room_cost + food_cost

        invoice = Invoice.objects.create(
            user=booking.user,
            booking=booking,
            amount=total_amount
        )
        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        invoice = serializer.validated_data['invoice']
        if self.request.user.role != 'ADMIN' and self.request.user.role != 'STAFF' and invoice.user != self.request.user:
             raise exceptions.PermissionDenied("You cannot pay someone else's invoice")
        
        payment = serializer.save()
        # Check if fully paid
        total_paid = sum(p.amount for p in invoice.payments.all())
        if total_paid >= invoice.amount:
            invoice.status = 'PAID'
            invoice.save()

from django.db.models import Sum
from rest_framework.views import APIView

class RevenueView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_revenue = Invoice.objects.filter(status='PAID').aggregate(total=Sum('amount'))['total'] or 0
        return Response({'total_revenue': total_revenue})
