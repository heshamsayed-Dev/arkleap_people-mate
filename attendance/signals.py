from django.db.models.signals import pre_save
from django.dispatch import receiver

from attendance.models.attendance_detail_model import AttendanceDetail
from attendance.models.attendance_model import Attendance
from employee.models.employee_model import Employee
@receiver(pre_save, sender=AttendanceDetail)
def attendance_detail_pre_save(sender, instance, **kwargs):
    if not instance.id:
        # print(f"kwargs dict is {kwargs}")
        # print("from pre save function")
        # print("context 123123")
        # print(model_to_dict(kwargs.get('signal')))
        # print(f"instance is {instance}")
        # print(instance.context.get('employee'))
        # employee=instance.employee
        employee=Employee.objects.get(id=3)
        try:
            attendance = Attendance.objects.get(date=instance.check_in.date(), employee=employee)
        except Attendance.DoesNotExist:
            attendance = Attendance.objects.create(
                date=instance.check_in.date(), employee=employee, check_in=instance.check_in
            )
        instance.attendance = attendance
