from rest_framework import serializers
from employee.models.employee_model import Employee
from people_mate.users.api.serializers import UserSerializer
class EmployeeSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    class Meta:
      model=Employee  
      fields = '__all__'
      extra_kwargs={
            'updated_by': {'write_only': True},
            'created_at' : {'write_only':True},
            'updated_at' : {'write_only':True},
        }

