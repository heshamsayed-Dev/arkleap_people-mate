from django.db import models


class Attendance(models.Model):
    employee = models.CharField(max_length=255)
    date = models.DateField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True)
    worked_hours = models.FloatField(null=True)
    default_check_in = models.FloatField(null=True)
    default_check_out = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
