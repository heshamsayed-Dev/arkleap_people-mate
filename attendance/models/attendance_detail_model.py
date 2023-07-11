from django.db import models

from .attendance_model import Attendance
from employee.models.company_branch_model import CompanyBranch

class AttendanceDetail(models.Model):
    branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name="attendance_details", blank=True)
