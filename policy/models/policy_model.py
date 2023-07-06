from datetime import date

from django.db import models

from employee.models.company_model import Company

from .common_model import CommonModel


class Policy(CommonModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_policies")
    working_hours = models.IntegerField()
    start_of_working_hours = models.TimeField()
    end_of_working_hours = models.TimeField()
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
