from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffSalaryViewSet, PayrollRecordViewSet

router = DefaultRouter()
router.register(r'salaries', StaffSalaryViewSet)
router.register(r'records', PayrollRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
