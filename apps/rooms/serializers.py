from rest_framework import serializers
from .models import Room, RoomType

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    room_type_name = serializers.ReadOnlyField(source='room_type.name')
    price = serializers.ReadOnlyField(source='room_type.price_per_night')
    capacity = serializers.ReadOnlyField(source='room_type.capacity')

    class Meta:
        model = Room
        fields = ('id', 'number', 'room_type', 'room_type_name', 'price', 'status', 'capacity')
        # Note: capacity is on RoomType, but might be useful to expose here if logic requires specific room tweaks.
        # But for now, we'll just get price/name from type.
