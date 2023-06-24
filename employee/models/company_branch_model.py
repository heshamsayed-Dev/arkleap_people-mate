from company_model import Company
from django.db import models


class CompanyBranch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
