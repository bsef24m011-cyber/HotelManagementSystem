from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.rooms.models import Room, RoomType
from apps.bookings.models import Booking
import datetime

User = get_user_model()

class BookingTests(APITestCase):
    def setUp(self):
        # Users
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.admin = User.objects.create_superuser(username='admin', password='password')
        
        # Room
        self.room_type = RoomType.objects.create(name='Standard', price_per_night=100, capacity=2)
        self.room = Room.objects.create(number='101', room_type=self.room_type)
        
        # Dates
        self.today = datetime.date.today()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.day_after = self.today + datetime.timedelta(days=2)
        self.next_week = self.today + datetime.timedelta(days=7)

    def test_create_booking_success(self):
        """
        Ensure we can create a valid booking.
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse('booking-list')
        data = {
            'room': self.room.id,
            'check_in_date': self.today,
            'check_out_date': self.tomorrow
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().user, self.user1)

    def test_create_booking_invalid_dates(self):
        """
        Ensure check-out must be after check-in.
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse('booking-list')
        data = {
            'room': self.room.id,
            'check_in_date': self.tomorrow,
            'check_out_date': self.today # Invalid
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_past_dates(self):
        """
        Ensure check-in cannot be in the past.
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse('booking-list')
        yesterday = self.today - datetime.timedelta(days=1)
        data = {
            'room': self.room.id,
            'check_in_date': yesterday,
            'check_out_date': self.today
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overlap_protection(self):
        """
        Ensure we cannot book a room that is already booked (Confirmed/Pending).
        """
        # Create existing booking
        Booking.objects.create(
            user=self.user1,
            room=self.room,
            check_in_date=self.today,
            check_out_date=self.day_after,
            status='CONFIRMED'
        )
        
        # Try to book overlapping dates (start inside existing)
        self.client.force_authenticate(user=self.user2)
        url = reverse('booking-list')
        data = {
            'room': self.room.id,
            'check_in_date': self.tomorrow, # Inside user1's booking
            'check_out_date': self.next_week
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Room is already booked', str(response.data))

    def test_permission_isolation(self):
        """
        Ensure users only see their own bookings, admin sees all.
        """
        # User 1 booking
        b1 = Booking.objects.create(user=self.user1, room=self.room, check_in_date=self.today, check_out_date=self.tomorrow)
        # User 2 booking
        b2 = Booking.objects.create(user=self.user2, room=self.room, check_in_date=self.next_week, check_out_date=self.next_week + datetime.timedelta(days=1))
        
        url = reverse('booking-list')
        
        # User 1 checks list
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], b1.id)
        
        # Admin checks list
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
