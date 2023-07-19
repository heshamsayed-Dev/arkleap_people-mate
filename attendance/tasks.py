from datetime import datetime

from attendance.constants import STATUS_CLOSED, STATUS_OPEN
from attendance.models.attendance_model import Attendance
from attendance.views.utils import calculate_checkout_time, calculate_worked_hours
from config.celery_app import app


@app.task
def calculate_attendance_task():
    returned_attendances = []
    attendances = Attendance.objects.prefetch_related("attendance_details").get(status=STATUS_OPEN)
    for attendance in attendances:
        # get the transaction that its check out field is not set
        detail_with_no_check_out = attendance.attendance_details.filter(check_out=None).first()
        # add the attendance that has transaction with no check out
        if detail_with_no_check_out:
            returned_attendances.append(attendance)

        # case if shift in 2 days it will skip calculating this attendance if the task
        # is running at the start of its shift
        elif attendance.shift_start_time > attendance.shift_end_time and attendance.date == datetime.today().date():
            pass

        else:
            attendance.check_out = calculate_checkout_time(attendance.attendance_details)
            attendance.worked_hours = calculate_worked_hours(attendance.attendance_details)
            attendance.status = STATUS_CLOSED
            attendance.save()

    return returned_attendances
