from django.contrib import admin

from .models.company_branch_model import CompanyBranch
from .models.company_model import Company
from .models.employee_model import Employee

# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyBranch)
admin.site.register(Employee)
