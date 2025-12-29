from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.rooms.models import Room, RoomType
from apps.bookings.models import Booking
from apps.food.models import FoodItem, FoodOrder
import datetime

User = get_user_model()

class FoodTests(APITestCase):
    def setUp(self):
        # Users
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.admin = User.objects.create_superuser(username='admin', password='password')
        
        # Setup Booking for User 1
        self.room_type = RoomType.objects.create(name='Standard', price_per_night=100, capacity=2)
        self.room = Room.objects.create(number='101', room_type=self.room_type)
        self.booking = Booking.objects.create(
            user=self.user1,
            room=self.room,
            check_in_date=datetime.date.today(),
            check_out_date=datetime.date.today() + datetime.timedelta(days=1),
            status='CONFIRMED'
        )
        
        # Initial Food Item
        self.food_item = FoodItem.objects.create(name='Burger', price=10.00)

    def test_create_food_item_admin(self):
        """Admin can create food items"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('fooditem-list')
        data = {'name': 'Pizza', 'price': 15.00}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_food_item_user_forbidden(self):
        """User cannot create food items"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('fooditem-list')
        data = {'name': 'Pizza', 'price': 15.00}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_food_success(self):
        """User can order food for their booking"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('foodorder-list')
        data = {
            'booking': self.booking.id,
            'items': [
                {'food_item': self.food_item.id, 'quantity': 2}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FoodOrder.objects.count(), 1)
        self.assertEqual(FoodOrder.objects.get().items.first().quantity, 2)

    def test_order_food_wrong_user_forbidden(self):
        """User CANNOT order food for someone else's booking"""
        self.client.force_authenticate(user=self.user2) # Different user
        url = reverse('foodorder-list')
        data = {
            'booking': self.booking.id, # User1's booking
            'items': [
                {'food_item': self.food_item.id, 'quantity': 1}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
