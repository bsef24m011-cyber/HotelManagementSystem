from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.payroll.models import StaffSalary, PayrollRecord

User = get_user_model()

class PayrollTests(APITestCase):
    def setUp(self):
        # Users
        self.admin = User.objects.create_superuser(username='admin', password='password', role='ADMIN')
        self.staff1 = User.objects.create_user(username='staff1', password='password', role='STAFF')
        self.staff2 = User.objects.create_user(username='staff2', password='password', role='STAFF')
        self.customer = User.objects.create_user(username='customer', password='password', role='CUSTOMER')
        
        # Salary
        self.salary1 = StaffSalary.objects.create(staff=self.staff1, base_salary=5000.00)
        self.salary2 = StaffSalary.objects.create(staff=self.staff2, base_salary=6000.00)
        
        # Record
        self.record1 = PayrollRecord.objects.create(staff=self.staff1, amount_paid=5000.00)

    def test_salary_access_admin(self):
        """Admin sees all salaries"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('staffsalary-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_salary_access_staff(self):
        """Staff sees only their own salary"""
        self.client.force_authenticate(user=self.staff1)
        url = reverse('staffsalary-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['staff_name'], 'staff1')

    def test_salary_access_customer(self):
        """Customer cannot access salaries"""
        self.client.force_authenticate(user=self.customer)
        url = reverse('staffsalary-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_record_visibility(self):
        """Staff sees only their own payment records"""
        self.client.force_authenticate(user=self.staff1)
        url = reverse('payrollrecord-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        
        self.client.force_authenticate(user=self.staff2)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)
