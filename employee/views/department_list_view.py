from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from employee.models.department_model import Department
from employee.serializers.department_serializer import DepartmentSerializer

from .utils import get_model_by_pk


class DepartmentListView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                department = get_model_by_pk("Department", pk)
                serializer = DepartmentSerializer(department)
            else:
                departments = Department.objects.all()
                serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data)

        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
