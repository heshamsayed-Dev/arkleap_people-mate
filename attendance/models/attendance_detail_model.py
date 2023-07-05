from django.db import models

from .attendance_model import Attendance


class AttendanceDetail(models.Model):
    branch = models.CharField(max_length=255)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name="attendance_details", blank=True)
