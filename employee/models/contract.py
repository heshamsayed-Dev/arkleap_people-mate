from django.db import models
from .employee_model import Employee
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