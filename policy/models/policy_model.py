from django.db import models
from employee.models.company_model import Company
from .common_model import CommonModel


class Policy(CommonModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_policies")
    working_hours = models.IntegerField()
    working_policy_start_date = models.TimeField(blank=True, null=True)
    working_policy_end_date = models.TimeField(blank=True, null=True)
