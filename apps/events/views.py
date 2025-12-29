from rest_framework import viewsets, permissions
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.role == 'STAFF':
            return Event.objects.all()
        return Event.objects.filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
