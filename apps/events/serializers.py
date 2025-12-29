from rest_framework import serializers
from .models import Event
import datetime

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('client', 'status', 'created_at')

    def validate(self, data):
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if date and date < datetime.date.today():
            raise serializers.ValidationError("Event date cannot be in the past.")

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")
        
        # Check overlap
        if date and start_time and end_time:
            overlapping = Event.objects.filter(
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time,
                status__in=['PENDING', 'CONFIRMED']
            )
            if self.instance:
                overlapping = overlapping.exclude(pk=self.instance.pk)
            
            if overlapping.exists():
                raise serializers.ValidationError("An event is already scheduled for this time slot.")

        return data
