from rest_framework import viewsets,generics
from employee.serializers.employee_serializer import EmployeeSerializer
from employee.models.employee_model import Employee
from datetime import datetime
from rest_framework.response import Response
class EmployeeUpdateView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


    def patch(self, request, *args, **kwargs):
        data = dict(request.data)

        instance = self.get_object()
        data['updated_by'] = request.user.id
        data['updated_at'] = datetime.now()
        return Response(data)

      

