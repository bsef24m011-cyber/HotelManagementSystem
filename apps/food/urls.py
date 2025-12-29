from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodItemViewSet, FoodOrderViewSet

router = DefaultRouter()
router.register(r'items', FoodItemViewSet)
router.register(r'orders', FoodOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
