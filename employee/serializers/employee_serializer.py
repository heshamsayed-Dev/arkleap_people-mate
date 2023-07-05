from rest_framework import serializers
from employee.models.employee_model import Employee
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
      model=Employee  
      fields = '__all__'
      

