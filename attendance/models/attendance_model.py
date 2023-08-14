from django.db import models

from attendance.constants import STATUS_CHOICES
from employee.models.company_model import Company
from employee.models.employee_model import Employee


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee")
    date = models.DateField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True)
    worked_hours = models.FloatField(null=True)
    shift_start_time = models.TimeField(null=True)
    shift_end_time = models.TimeField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
