from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.constants import STATUS_CLOSED
from attendance.models.attendance_model import Attendance

from .utils import calculate_checkout_time, calculate_worked_hours


class AttendanceCalculateView(APIView):
    def get(self, request, pk):
        try:
            attendance = Attendance.objects.prefetch_related("attendance_details").get(id=pk)
            # get the transaction that its check out field is not set
            detail_with_no_check_out = attendance.attendance_details.filter(check_out=None).first()

            # if there is no check out set in the attendance's  last transaction
            if detail_with_no_check_out:
                raise ValueError("there is a transaction required data not completed ")

            # checks if attendance has transaction
            if attendance.attendance_details.all():
                attendance.check_out = calculate_checkout_time(attendance.attendance_details.all())
                attendance.worked_hours = calculate_worked_hours(attendance.attendance_details.all())
            else:
                raise ValueError(
                    "there is no attendance details . each Attendance should have at least 1 transaction "
                )

            attendance.status = STATUS_CLOSED
            attendance.save()

            return Response(data={"message": "Attendance Details calculated successfully"}, status=200)
        except Attendance.DoesNotExist:
            return Response({"message": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
