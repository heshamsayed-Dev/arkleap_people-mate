from rest_framework import serializers
from employee.models.company_model import Company
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
      model=Company  
      fields = '__all__'
   