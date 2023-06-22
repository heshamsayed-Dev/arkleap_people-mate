from django.db import models
from .employee_model import Employee
class Dependency(models.Model):
    name=models.CharField(max_length=60,verbose_name='Name')
    relation=models.CharField()
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='dependencies')
    mobile=models.IntegerField(verbose_name='Mobile')
    relation=models.CharField(choices=(
        ('parent', 'Parent'),
        ('child', 'Child'),
        ('wife','Wife'),
    ),max_length=8 , verbose_name='Relation')
