from django.db import models
from .employee_model import Employee
from people_mate.users.models import User
class Contract(models.Model):
    department=models.CharField(max_length=30,verbose_name='Department relation')
    salary_structure=models.CharField(max_length=30,verbose_name='Salary Structure relation')
    employee_type=models.CharField(choices=(
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    ),max_length=10 , verbose_name='Employee Type' )
    position=models.CharField(max_length=30,verbose_name='Position')
    contract_type=models.CharField(max_length=30,verbose_name='Contract Type')
    start_date=models.DateField(verbose_name='Start Date')
    end_date=models.DateField(verbose_name='End Date')
    payment_type=models.CharField(verbose_name='Payment Relation')
    employee=models.ForeignKey(Employee ,on_delete=models.CASCADE ,related_name='contracts')
    created_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='created_contracts',null=True)
    updated_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='updated_contracts',null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)