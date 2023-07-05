from rest_framework import viewsets,generics
from employee.serializers.employee_serializer import EmployeeSerializer
from employee.models.employee_model import Employee
from datetime import datetime
from rest_framework.response import Response
from django.http import  QueryDict
class EmployeeUpdateView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        query_dict = QueryDict('', mutable=True)
        query_dict.update(request.data)
        query_dict['updated_by'] = request.user.id
        query_dict['updated_at'] = datetime.now()
        serializer = self.get_serializer(instance,data=query_dict,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        query_dict = QueryDict('', mutable=True)
        query_dict.update(request.data)
        query_dict['updated_by'] = request.user.id
        query_dict['updated_at'] = datetime.now()
        serializer = self.get_serializer(instance,data=query_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)    


      

