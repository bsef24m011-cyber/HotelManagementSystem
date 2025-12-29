from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', TemplateView.as_view(template_name='frontend/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='frontend/register.html'), name='register'),
    path('dashboard/', TemplateView.as_view(template_name='frontend/dashboard.html'), name='dashboard'),
    path('rooms/', TemplateView.as_view(template_name='frontend/rooms.html'), name='rooms'),
    path('bookings/', TemplateView.as_view(template_name='frontend/bookings.html'), name='bookings'),
    path('food/', TemplateView.as_view(template_name='frontend/dining.html'), name='food'),
    path('', TemplateView.as_view(template_name='frontend/login.html'), name='home'),
]
