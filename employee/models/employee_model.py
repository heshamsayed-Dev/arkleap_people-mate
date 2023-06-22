from django.db import models
from people_mate.users.models import User
class Employee(models.Model):
    name=models.CharField(max_length=60,verbose_name='Employee Name')
    number=models.CharField(max_length=10,verbose_name='Employee Code')
    birth_date=models.DateField(verbose_name='Birth Date')
    email=models.CharField(max_length=20,verbose_name='Email')
    gender = models.CharField(choices=(('M', 'Male'),('F', 'Female')),max_length=6,verbose_name='Gender' )
    picture=models.FileField(upload_to='employee_pictures/',verbose_name='Picture')
    hire_date=models.DateField(verbose_name='Hire Date')
    termination_date=models.DateField(verbose_name='Termination Date',null=True)
    address_1=models.CharField(max_length=120,verbose_name='Address 1')
    address_2 = models.CharField(max_length=120,verbose_name='Address 2')
    phone=models.IntegerField(verbose_name='Phone',null=True)
    mobile=models.IntegerField(verbose_name='Mobile')
    birth_place=models.CharField(max_length=120,verbose_name='Place of Birth')
    nationality=models.CharField(max_length=15,verbose_name='Nationality')
    id_type=models.CharField(max_length=15,verbose_name='ID Type')
    id_number=models.CharField(max_length=15,verbose_name='ID Number')

    has_medical=models.BooleanField(verbose_name='Has Medical')
    has_insurance=models.BooleanField(verbose_name='Has Insurance')
    medical_start_date=models.DateField(verbose_name='Medical Start Date',null=True)
    medical_end_date=models.DateField(verbose_name='Medical End Date',null=True)
    medical_number=models.CharField(max_length=30,verbose_name='Medical Number',null=True)
    insurance_date=models.DateField(verbose_name='Insurance Date',null=True)
    insurance_number=models.CharField(max_length=30,verbose_name='Insurance Number',null=True)
    insurance_salary=models.FloatField(verbose_name='Insurance Salary',null=True)
    retirement_insurance_salary=models.FloatField(verbose_name='Retirement Insurance Salary',null=True)


    social_status=models.CharField(choices=(
        ('single', 'Single'),
        ('married', 'Married'),
        ('engaged','Engaged'),
        ('divorced','Divorced'),
        ('widowed','Widowed'),
    ),max_length=10 , verbose_name='Social Status' )
    military_status=models.CharField(choices=(
        ('finished', 'Finished'),
        ('exempted', 'Exempted'),
        ('postponed','Postponed'),
    ),max_length=12 , verbose_name='Military Status' )
    religion=models.CharField(choices=(
        ('muslim', 'Muslim'),
        ('christian', 'Christian'),
    ),max_length=10 )
    study_field=models.CharField(max_length=15,verbose_name='Field Of Study')
    education_degree=models.CharField(choices=(
        ('bachelor', 'Bachelor'),
        ('diploma', 'Diploma'),
        ('masters','Masters'),
    ),max_length=12 )
    is_active=models.BooleanField(verbose_name='Is Active ')
    manager=models.ForeignKey('self',on_delete=models.SET_NULL,related_name='employees',null=True)
    created_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='created_employees',null=True)
    updated_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='updated_employees',null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)


    


