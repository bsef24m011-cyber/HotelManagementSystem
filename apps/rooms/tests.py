from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.rooms.models import Room, RoomType

User = get_user_model()

class RoomTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin = User.objects.create_superuser(username='adminuser', password='adminpassword')
        
        self.room_type = RoomType.objects.create(
            name='Deluxe',
            description='A deluxe room',
            price_per_night=100.00,
            capacity=2
        )
        self.room = Room.objects.create(
            number='101',
            room_type=self.room_type,
            status='AVAILABLE'
        )

    def test_list_rooms(self):
        """
        Ensure we can list rooms.
        """
        url = reverse('room-list') # Default router basename is 'room' by default logic
        
        # Test unobtanium: Default router namesets
        # 'types' -> RoomTypeViewSet
        # '' -> RoomViewSet -> basename 'room' if not specified? 
        # Actually, let's verify basename. If no basename provided to router.register, 
        # it uses model name lowercased. So 'room-list'.
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if capacity is present (the fix)
        self.assertEqual(response.data[0]['capacity'], 2)

    def test_create_room_type_admin(self):
        """
        Ensure admin can create room types.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse('roomtype-list')
        data = {
            'name': 'Suite',
            'description': 'Luxury suite',
            'price_per_night': 500.00,
            'capacity': 4
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_room_type_user_fail(self):
        """
        Ensure non-admin cannot create room types (IsAuthenticatedOrReadOnly).
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('roomtype-list')
        data = {'name': 'Basic', 'price_per_night': 50, 'capacity': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
