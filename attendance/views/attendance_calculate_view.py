from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.serializers.attendance_serializer import AttendanceSerializer
from attendance.models.attendance_model import Attendance
from .utils import calculate_checkout_time , calculate_worked_hours

class AttendanceCalculateView(APIView):

    def get(self, request, pk):
        try:
            attendance = Attendance.objects.prefetch_related('attendance_details').get(id=pk)
            detail_hasnt_check_out=attendance.attendance_details.filter(check_out=None).first()
            if attendance.status == 'closed':
                raise ValueError(f"this attendance is already closed. ")
    
            if detail_hasnt_check_out and not  attendance.check_out :
                raise ValueError(f"there is no attendance details for this date ")

            if attendance.attendance_details.all():
                if detail_hasnt_check_out and  attendance.check_out :
                    detail_hasnt_check_out.check_out=attendance.check_out
                    detail_hasnt_check_out.save()
                else:       
                    attendance.check_out=calculate_checkout_time(attendance.attendance_details.all())

                attendance.worked_hours=calculate_worked_hours(attendance.attendance_details.all())

            attendance.status='closed'
            attendance.save()

            return Response(
                data={"message": "Attendance Details calculated successfully"}, status=200
            )     
        except Attendance.DoesNotExist:
            return Response({"message": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


