from django.db import models

from employee.constants import LOCATION_STATUS_CHOICES

from .company_branch_model import CompanyBranch


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=15, choices=LOCATION_STATUS_CHOICES)
    branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, related_name="locations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
