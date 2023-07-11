from django.contrib import admin

from .models.company_branch_model import CompanyBranch
from .models.company_model import Company
from .models.employee_model import Employee
from .models.department_model import Department
from .models.location_model import Location
from .models.position_model import Position
# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyBranch)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Position)

