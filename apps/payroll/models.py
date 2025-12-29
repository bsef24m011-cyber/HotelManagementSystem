from django.db import models
from django.conf import settings

class StaffSalary(models.Model):
    staff = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='salary_info', limit_choices_to={'role__in': ['STAFF', 'ADMIN']})
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Salary for {self.staff.username}"

class PayrollRecord(models.Model):
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Payment of {self.amount_paid} to {self.staff.username} on {self.payment_date}"
