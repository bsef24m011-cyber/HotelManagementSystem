from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.events.models import Event
import datetime

User = get_user_model()

class EventTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.admin = User.objects.create_superuser(username='admin', password='password')
        
        self.today = datetime.date.today()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.future_date = self.today + datetime.timedelta(days=10)

    def test_create_event_success(self):
        """Ensure we can create a valid event"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('event-list')
        data = {
            'event_type': 'WEDDING',
            'date': self.future_date,
            'start_time': '14:00:00',
            'end_time': '18:00:00',
            'attendees': 50,
            'price': 1000.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().client, self.user1)

    def test_create_event_invalid_time(self):
        """End time must be after start time"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('event-list')
        data = {
            'event_type': 'PARTY',
            'date': self.future_date,
            'start_time': '18:00:00',
            'end_time': '14:00:00', # Invalid
            'attendees': 20,
            'price': 500.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_past_date(self):
        """Cannot schedule events in the past"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('event-list')
        yesterday = self.today - datetime.timedelta(days=1)
        data = {
            'event_type': 'CONFERENCE',
            'date': yesterday,
            'start_time': '10:00:00',
            'end_time': '12:00:00',
            'attendees': 10,
            'price': 100.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overlap_protection(self):
        """Cannot schedule overlapping events"""
        # Create existing event
        Event.objects.create(
            client=self.user1,
            event_type='WEDDING',
            date=self.future_date,
            start_time='14:00:00',
            end_time='18:00:00',
            attendees=100,
            price=2000.00,
            status='CONFIRMED'
        )
        
        # Try to schedule overlap (16:00 - 20:00)
        self.client.force_authenticate(user=self.user2)
        url = reverse('event-list')
        data = {
            'event_type': 'PARTY',
            'date': self.future_date,
            'start_time': '16:00:00', # Overlaps
            'end_time': '20:00:00',
            'attendees': 30,
            'price': 600.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already scheduled', str(response.data))

    def test_permission_isolation(self):
        """Users see only their events"""
        Event.objects.create(client=self.user1, event_type='WEDDING', date=self.future_date, start_time='10:00', end_time='12:00', attendees=10, price=100)
        Event.objects.create(client=self.user2, event_type='PARTY', date=self.future_date, start_time='14:00', end_time='16:00', attendees=10, price=100)
        
        url = reverse('event-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event_type'], 'WEDDING')
