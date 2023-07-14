from django.db import models

from employee.models.employee_model import Employee

status_choices = (("open", "Open"), ("closed", "Closed"))
creation_choices = (("manual", "Manual"), ("automatic", "Automatic"))


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee")
    date = models.DateField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True)
    worked_hours = models.FloatField(null=True)
    shift_start_time = models.TimeField(null=True)
    shift_end_time = models.TimeField(null=True)
    status = models.CharField(max_length=15, choices=status_choices)
    creation_method = models.CharField(max_length=15, choices=creation_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
