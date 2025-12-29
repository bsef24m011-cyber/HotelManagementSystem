from rest_framework import serializers
from .models import Invoice, Payment
from apps.bookings.models import Booking
from apps.events.models import Event

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('payment_date',)

class InvoiceSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('amount', 'issued_date')

    # Logic to generate amount could be in a view or signal, but usually computed on creation
