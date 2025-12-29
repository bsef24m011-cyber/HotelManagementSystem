from rest_framework import generics, permissions, viewsets
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(role='CUSTOMER')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

from rest_framework.views import APIView
from rest_framework.response import Response
from apps.bookings.serializers import BookingSerializer
from apps.events.serializers import EventSerializer
from apps.food.serializers import FoodOrderSerializer

class ServiceHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        bookings = user.bookings.all()
        events = user.events.all()
        # Food orders are linked to bookings, but we can also fetch them if we want a flat list
        # For now, return bookings and events
        data = {
            'bookings': BookingSerializer(bookings, many=True).data,
            'events': EventSerializer(events, many=True).data
        }
        return Response(data)
