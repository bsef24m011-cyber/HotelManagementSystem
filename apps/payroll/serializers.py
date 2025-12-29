from rest_framework import serializers
from .models import StaffSalary, PayrollRecord

class StaffSalarySerializer(serializers.ModelSerializer):
    staff_name = serializers.ReadOnlyField(source='staff.username')

    class Meta:
        model = StaffSalary
        fields = ('id', 'staff', 'staff_name', 'base_salary', 'bonus')

class PayrollRecordSerializer(serializers.ModelSerializer):
    staff_name = serializers.ReadOnlyField(source='staff.username')

    class Meta:
        model = PayrollRecord
        fields = ('id', 'staff', 'staff_name', 'amount_paid', 'payment_date', 'description')
