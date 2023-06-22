from django.db import models
from .employee_model import Employee
class EmployeeAttachment(models.Model):
    name=models.CharField(max_length=60,verbose_name='Name')
    category=models.CharField(verbose_name='Category')
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='attachments')
    expiration_date=models.DateField()
    attachment=models.FileField(upload_to='employee_attachments/')
