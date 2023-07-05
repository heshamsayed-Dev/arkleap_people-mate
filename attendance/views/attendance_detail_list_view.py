from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models.attendance_detail_model import AttendanceDetail
from attendance.serializers.attendance_detail_serializer import AttendanceDetailSerializer

from .utils import get_model_by_pk


class AttendanceDetailListView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                attendance_detail = get_model_by_pk("AttendanceDetail", pk)
                serializer = AttendanceDetailSerializer(attendance_detail)
            else:
                attendance_details = AttendanceDetail.objects.all()
                serializer = AttendanceDetailSerializer(attendance_details, many=True)
            return Response(serializer.data)

        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
