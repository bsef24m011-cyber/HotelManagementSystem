from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, RoomTypeViewSet

router = DefaultRouter()
router.register(r'types', RoomTypeViewSet)
router.register(r'', RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
