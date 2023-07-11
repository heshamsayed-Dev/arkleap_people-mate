from django.contrib import admin

from .models.attendance_model import Attendance
from .models.attendance_detail_model import AttendanceDetail


admin.site.register(Attendance)
admin.site.register(AttendanceDetail)
