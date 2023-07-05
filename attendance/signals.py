from django.db.models.signals import pre_save
from django.dispatch import receiver

from attendance.models.attendance_detail_model import AttendanceDetail
from attendance.models.attendance_model import Attendance


@receiver(pre_save, sender=AttendanceDetail)
def attendance_detail_pre_save(sender, instance, **kwargs):
    if not instance.id:
        try:
            attendance = Attendance.objects.get(date=instance.check_in.date(), employee="employee")
        except Attendance.DoesNotExist:
            attendance = Attendance.objects.create(
                date=instance.check_in.date(), employee="employee", check_in=instance.check_in
            )
        instance.attendance = attendance
