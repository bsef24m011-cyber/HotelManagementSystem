from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Luxuria Management"
admin.site.site_title = "Luxuria Management Portal"
admin.site.index_title = "Welcome to Luxuria Hotel Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    # App URLs will be included here once created
    path('api/users/', include('apps.users.urls')),
    path('api/rooms/', include('apps.rooms.urls')),
    path('api/bookings/', include('apps.bookings.urls')),
    path('api/food/', include('apps.food.urls')),
    path('api/events/', include('apps.events.urls')),
    path('api/billing/', include('apps.billing.urls')),
    path('api/payroll/', include('apps.payroll.urls')),
    path('', include('frontend.urls')),  # Frontennd
]
