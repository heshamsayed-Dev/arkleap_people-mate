from django.http import QueryDict
from rest_framework import generics, status
from rest_framework.response import Response

from employee.models.employee_model import Employee
from employee.serializers.employee_serializer import EmployeeSerializer


class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        query_dict = QueryDict("", mutable=True)
        query_dict.update(request.data)
        query_dict["created_by"] = request.user.id
        serializer = self.get_serializer(data=query_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
