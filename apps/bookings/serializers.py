from rest_framework import serializers
from .models import Booking
from apps.rooms.serializers import RoomSerializer, Room
import datetime

class BookingSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    room_number = serializers.CharField(source='room.number', read_only=True)
    room_details = RoomSerializer(source='room', read_only=True)
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at', 'updated_at')

    def validate(self, data):
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        room = data.get('room')

        if check_in >= check_out:
            raise serializers.ValidationError("Check-out date must be after check-in date.")

        if check_in < datetime.date.today():
             raise serializers.ValidationError("Check-in date cannot be in the past.")

        # Double booking check
        overlapping_bookings = Booking.objects.filter(
            room=room,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in,
            status__in=['PENDING', 'CONFIRMED']
        )
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Room is already booked for these dates.")

        return data
