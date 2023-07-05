from django.urls import path

from attendance.views.attendance_detail_create_view import AttendanceDetailCreateView
from attendance.views.attendance_detail_delete_view import AttendanceDetailDeleteView
from attendance.views.attendance_detail_list_view import AttendanceDetailListView
from attendance.views.attendance_detail_update_view import AttendanceDetailUpdateView

urlpatterns = [
    path("", AttendanceDetailListView.as_view(), name="attendance_detail_list"),
    path("<int:pk>", AttendanceDetailListView.as_view(), name="attendance_detail_get"),
    path("create", AttendanceDetailCreateView.as_view(), name="attendance_detail_create"),
    path("<int:pk>/update", AttendanceDetailUpdateView.as_view(), name="attendance_detail_update"),
    path("<int:pk>/delete", AttendanceDetailDeleteView.as_view(), name="attendance_detail_delete"),
]
