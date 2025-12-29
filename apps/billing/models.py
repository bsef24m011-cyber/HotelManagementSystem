from django.db import models
from django.conf import settings
from apps.bookings.models import Booking
from apps.events.models import Event

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNPAID')

    def __str__(self):
        return f"Invoice {self.id} - {self.user.username} - {self.amount}"

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('CREDIT_CARD', 'Credit Card'),
        ('ONLINE', 'Online'),
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Payment {self.id} for Invoice {self.invoice.id}"
