from rest_framework import viewsets,generics,status
from employee.serializers.employee_serializer import EmployeeSerializer
from employee.models.employee_model import Employee
from rest_framework.response import Response
class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        data['created_by'] = request.user.id
        return Response(data)



    