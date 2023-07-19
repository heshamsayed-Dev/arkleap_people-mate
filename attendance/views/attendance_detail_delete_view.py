from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.constants import STATUS_OPEN

from .utils import get_model_by_pk


class AttendanceDetailDeleteView(APIView):
    def delete(self, request, pk):
        try:
            attendance_detail = get_model_by_pk("AttendanceDetail", pk)
            attendance = attendance_detail.attendance
            attendance.status = STATUS_OPEN
            attendance_detail.delete()
            attendance.save()
            return Response(
                data={"message": "Attendance Detail deleted successfully"}, status=status.HTTP_204_NO_CONTENT
            )
        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
