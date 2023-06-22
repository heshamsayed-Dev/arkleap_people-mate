from django.db import models
from .employee_model import Employee
from people_mate.users.models import User
class EmployeeAttachment(models.Model):
    name=models.CharField(max_length=60,verbose_name='Name')
    category=models.CharField(verbose_name='Category')
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='attachments')
    expiration_date=models.DateField()
    attachment=models.FileField(upload_to='employee_attachments/')
    created_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='created_employee_attachments',null=True)
    updated_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='updated_employee_attachments',null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)
