from rest_framework import serializers
from employee.models.employee_model import Employee
from people_mate.users.api.serializers import UserSerializer
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
      model=Employee  
      fields = '__all__'
      extra_kwargs={
            'created_by':{'write_only': True},
            'updated_by': {'write_only': True},
            'created_at' : {'write_only':True},
            'updated_at' : {'write_only':True},
        }

