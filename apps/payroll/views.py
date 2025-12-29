from rest_framework import viewsets, permissions
from .models import StaffSalary, PayrollRecord
from .serializers import StaffSalarySerializer, PayrollRecordSerializer

class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'STAFF']

class StaffSalaryViewSet(viewsets.ModelViewSet):
    queryset = StaffSalary.objects.all()
    serializer_class = StaffSalarySerializer
    permission_classes = [IsAdminOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return StaffSalary.objects.all()
        return StaffSalary.objects.filter(staff=user)

class PayrollRecordViewSet(viewsets.ModelViewSet):
    queryset = PayrollRecord.objects.all()
    serializer_class = PayrollRecordSerializer
    permission_classes = [IsAdminOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return PayrollRecord.objects.all()
        return PayrollRecord.objects.filter(staff=user)
