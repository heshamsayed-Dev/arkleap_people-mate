from django.db import models
from people_mate.users.models import User
class Employee(models.Model):
    name=models.CharField(max_length=60,verbose_name='Employee Name')
    email=models.CharField(max_length=20,verbose_name='Email')
    mobile=models.IntegerField(verbose_name='Mobile')
    created_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='created_employees',null=True)
    updated_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='updated_employees',null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)


    


