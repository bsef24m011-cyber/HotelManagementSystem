from django.contrib import admin
from .models import FoodItem, FoodOrder, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'status', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(FoodItem)
admin.site.register(FoodOrder, FoodOrderAdmin)
