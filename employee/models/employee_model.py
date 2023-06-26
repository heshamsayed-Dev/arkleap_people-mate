from django.db import models

from people_mate.users.models import User

from .company_branch_model import CompanyBranch
from .company_model import Company
from .constants import DEVELOPMENT, SENIOR_SOFTWARE_ENGINEER, SOFTWARE_ENGINEER, TESTING

POSITIONS = ((SOFTWARE_ENGINEER, "Software engineer"), (SENIOR_SOFTWARE_ENGINEER, "senior software engineer"))

DEPARTMENT = ((DEVELOPMENT, "development"), (TESTING, "testing"))


# TODO pay attention to the spaces
class Employee(models.Model):
    name = models.CharField(max_length=60, verbose_name="Employee Name")
    email = models.CharField(max_length=128, verbose_name="Email")
    position = models.CharField(max_length=255, choices=POSITIONS)
    department = models.CharField(max_length=255, choices=DEPARTMENT)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)
    mobile = models.CharField(verbose_name="Mobile")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_employees", null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="updated_employees", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
