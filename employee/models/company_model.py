from django.db import models
from django.utils.text import slugify


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
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
    slug = models.SlugField(null=False, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
