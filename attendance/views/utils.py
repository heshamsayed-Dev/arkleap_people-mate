from django.apps import apps
from django.http import Http404
from datetime import datetime
from attendance.models.attendance_model import Attendance
from attendance.models.attendance_detail_model import AttendanceDetail

def get_model_by_pk(model_name, pk):
    model = apps.get_model("attendance", model_name)
    obj = model.objects.filter(pk=pk).first()
    if not obj:
        raise Http404(f"{model_name} not found")
    return obj

def calculate_checkout_time(details):
        checkout=details.first().check_out
        for det in details:
            if det.check_out > checkout:
                checkout=det.check_out
                
        return checkout


def calculate_worked_hours(details):
        worked_hours=0
        for det in details:
            worked_hours+=(det.check_out - det.check_in).total_seconds()/3600

        return worked_hours        


def calculate_attendances_daily():
    returned_atts=[]
    attendances = Attendance.objects.prefetch_related('attendance_details').get(status='open')
    for att in attendances:
        detail_hasnt_check_out=att.attendance_details.filter(check_out=None).first()
        if (not att.check_out) and detail_hasnt_check_out:
            returned_atts.append(att)
        
        elif att.shift_start_time > att.shift_end_time and att.date == datetime.today().date():
            pass

        else:
            if att.check_out and detail_hasnt_check_out:
                detail_hasnt_check_out.check_out=att.check_out
                detail_hasnt_check_out.save()
            else:    
                att.check_out = calculate_checkout_time(att.attendance_details)
            
            att.status='closed'
            att.worked_hours = calculate_worked_hours(att.attendance_details)
            att.save()

    return returned_atts        