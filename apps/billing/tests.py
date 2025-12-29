from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.rooms.models import Room, RoomType
from apps.bookings.models import Booking
from apps.food.models import FoodItem, FoodOrder, OrderItem
from apps.billing.models import Invoice, Payment
import datetime

User = get_user_model()

class BillingTests(APITestCase):
    def setUp(self):
        # Users
        self.user1 = User.objects.create_user(username='user1', password='password', role='CUSTOMER')
        self.user2 = User.objects.create_user(username='user2', password='password', role='CUSTOMER')
        self.admin = User.objects.create_superuser(username='admin', password='password', role='ADMIN')
        
        # Room
        self.room_type = RoomType.objects.create(name='Standard', price_per_night=100, capacity=2)
        self.room = Room.objects.create(number='101', room_type=self.room_type)
        
        # Booking (2 Nights = 200)
        self.booking = Booking.objects.create(
            user=self.user1,
            room=self.room,
            check_in_date=datetime.date.today(),
            check_out_date=datetime.date.today() + datetime.timedelta(days=2),
            status='CONFIRMED'
        )
        
        # Food (2 Burgers @ 10 = 20)
        self.food_item = FoodItem.objects.create(name='Burger', price=10.00)
        self.food_order = FoodOrder.objects.create(booking=self.booking, status='DELIVERED')
        OrderItem.objects.create(order=self.food_order, food_item=self.food_item, quantity=2)

    def test_generate_invoice(self):
        """Ensure invoice calculates total correctly (Room + Food)"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('invoice-generate-booking-invoice')
        data = {'booking_id': self.booking.id}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 200 (Room) + 20 (Food) = 220
        self.assertEqual(float(response.data['amount']), 220.00)

    def test_generate_invoice_forbidden(self):
        """User cannot generate invoice for another user's booking"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('invoice-generate-booking-invoice')
        data = {'booking_id': self.booking.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_payment_logic(self):
        """Full payment updates invoice status"""
        # Admin creates invoice
        invoice = Invoice.objects.create(user=self.user1, booking=self.booking, amount=220.00)
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('payment-list')
        data = {
            'invoice': invoice.id,
            'amount': 220.00,
            'payment_method': 'CASH'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, 'PAID')

    def test_payment_forbidden(self):
        """User cannot pay another user's invoice"""
        invoice = Invoice.objects.create(user=self.user1, booking=self.booking, amount=220.00)
        
        self.client.force_authenticate(user=self.user2)
        url = reverse('payment-list')
        data = {
            'invoice': invoice.id,
            'amount': 220.00,
            'payment_method': 'CASH'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_revenue_admin_only(self):
        """Only admin can access revenue"""
        invoice = Invoice.objects.create(user=self.user1, amount=100.00, status='PAID')
        
        url = reverse('revenue')
        
        # User 1 (Forbidden)
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin (Success)
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_revenue']), 100.00)
