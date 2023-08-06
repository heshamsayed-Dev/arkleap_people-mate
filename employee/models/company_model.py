from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    arabic_name = models.CharField(max_length=100)
    tax_number = models.BigIntegerField(unique=True)
    commercial_record = models.BigIntegerField(unique=True)
    address = models.TextField()
    phone = models.BigIntegerField()
    mobile = models.CharField(null=True)
    fax = models.BigIntegerField()
    email = models.EmailField()
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
