from django.db import models
from .employee_model import Employee
from people_mate.users.models import User
class Dependency(models.Model):
    name=models.CharField(max_length=60,verbose_name='Name')
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='dependencies')
    mobile=models.IntegerField(verbose_name='Mobile')
    relation=models.CharField(choices=(
        ('parent', 'Parent'),
        ('child', 'Child'),
        ('wife','Wife'),
    ),max_length=8 , verbose_name='Relation')

    created_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='created_employee_dependencies',null=True)
    updated_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='updated_employee_dependencies',null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)
