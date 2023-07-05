from rest_framework import serializers
from employee.models.company_branch_model import CompanyBranch
class CompanyBranchSerializer(serializers.ModelSerializer):
    class Meta:
      model=CompanyBranch  
      fields = '__all__'