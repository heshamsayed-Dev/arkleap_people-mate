from datetime import datetime

from attendance.models.attendance_model import Attendance
from attendance.views.utils import calculate_checkout_time, calculate_worked_hours
from config.celery_app import app


@app.task
def calculate_attendance_task():
    returned_atts = []
    attendances = Attendance.objects.prefetch_related("attendance_details").get(status="open")
    for att in attendances:
        detail_hasnt_check_out = att.attendance_details.filter(check_out=None).first()
        if (not att.check_out) and detail_hasnt_check_out:
            returned_atts.append(att)

        elif att.shift_start_time > att.shift_end_time and att.date == datetime.today().date():
            pass

        else:
            if att.check_out and detail_hasnt_check_out:
                detail_hasnt_check_out.check_out = att.check_out
                detail_hasnt_check_out.save()
            else:
                att.check_out = calculate_checkout_time(att.attendance_details)

            att.status = "closed"
            att.worked_hours = calculate_worked_hours(att.attendance_details)
            att.save()
    return returned_atts
