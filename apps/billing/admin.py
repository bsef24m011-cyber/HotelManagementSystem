from django.contrib import admin
from .models import Invoice, Payment

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'issued_date')
    inlines = [PaymentInline]

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment)
