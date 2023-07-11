from django.db import models

from people_mate.users.models import User

from .company_branch_model import CompanyBranch
from .company_model import Company
from .department_model import Department
from .position_model import Position


# TODO pay attention to the spaces
class Employee(models.Model):
    name = models.CharField(max_length=60, verbose_name="Employee Name")
    email = models.CharField(max_length=128, verbose_name="Email")
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)
    mobile = models.CharField(verbose_name="Mobile")
    user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_employees", null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="updated_employees", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    
