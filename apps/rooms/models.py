from django.db import models

class RoomType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(help_text="Number of people")

    def __str__(self):
        return self.name

class Room(models.Model):
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
        ('CLEANING', 'Cleaning'),
        ('MAINTENANCE', 'Maintenance'),
    )

    number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    
    def __str__(self):
        return f"Room {self.number} ({self.room_type.name})"
