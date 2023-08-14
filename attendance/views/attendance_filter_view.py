from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models.attendance_model import Attendance
from attendance.serializers.attendance_filter_serializer import AttendanceFilterSerializer
from attendance.serializers.attendance_serializer import AttendanceSerializer

from .utils import CustomPaginator


class AttendanceFilterView(APIView):
    def post(self, request):
        queryset = Attendance.objects.filter()
        filter_serializer = AttendanceFilterSerializer(data=request.data)
        if filter_serializer.is_valid():
            if request.data.get("employee"):
                queryset = queryset.filter(employee=request.data.get("employee"))
            if request.data.get("date_from"):
                queryset = queryset.filter(date__gte=request.data.get("date_from"))
            if request.data.get("date_to"):
                queryset = queryset.filter(date__lte=request.data.get("date_to"))

            paginator = CustomPaginator(1)
            paginated_attendances = paginator.paginate_queryset(queryset, request)
            serializer = AttendanceSerializer(paginated_attendances, many=True)
            return paginator.get_paginated_response(serializer.data)
            # serializer = AttendanceSerializer(queryset, many=True)
            # return Response(serializer.data)
        else:
            return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
