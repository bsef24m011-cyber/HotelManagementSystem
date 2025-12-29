from django.urls import path
from .views import RegisterView, UserProfileView, CustomerViewSet, ServiceHistoryView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customers/', CustomerViewSet.as_view({'get': 'list'}), name='customer_list'),
    path('history/', ServiceHistoryView.as_view(), name='service_history'),
]
