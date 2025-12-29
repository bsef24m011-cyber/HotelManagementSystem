from rest_framework import serializers
from .models import FoodItem, FoodOrder, OrderItem

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.ReadOnlyField(source='food_item.name')
    food_item_price = serializers.ReadOnlyField(source='food_item.price')

    class Meta:
        model = OrderItem
        fields = ('id', 'food_item', 'quantity', 'food_item_name', 'food_item_price')

class FoodOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = FoodOrder
        fields = ('id', 'booking', 'status', 'created_at', 'items', 'total_price')

    def get_total_price(self, obj):
        return sum(item.food_item.price * item.quantity for item in obj.items.all())

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = FoodOrder.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
