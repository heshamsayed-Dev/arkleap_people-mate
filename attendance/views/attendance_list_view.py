from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models.attendance_model import Attendance
from attendance.serializers.attendance_serializer import AttendanceSerializer

from .utils import get_model_by_pk


class AttendanceListView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                attendance = get_model_by_pk("Attendance", pk)
                serializer = AttendanceSerializer(attendance)
            else:
                attendances = Attendance.objects.all()
                serializer = AttendanceSerializer(attendances, many=True)
            return Response(serializer.data)

        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
