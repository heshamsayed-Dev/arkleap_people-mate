from datetime import date

from django.db import models

from config.settings import base
from employee.models.company_model import Company
from employee.models.position_model import Position


class CommonModel(models.Model):
    created_by = models.ForeignKey(
        base.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_created_%(class)s"
    )
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    last_update_by = models.ForeignKey(
        base.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="user_changed_%(class)s"
    )
    last_update_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Policy(CommonModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_policies")
    working_hours = models.IntegerField()
    start_of_working_hours = models.TimeField()
    end_of_working_hours = models.TimeField()
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)


class PositionPolicy(CommonModel):
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
    )
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)
    end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
