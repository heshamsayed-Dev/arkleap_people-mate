from rest_framework import viewsets,generics
from employee.serializers.employee_serializer import EmployeeSerializer
from employee.models.employee_model import Employee

class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer