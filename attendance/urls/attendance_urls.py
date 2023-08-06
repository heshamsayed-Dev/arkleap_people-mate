from django.urls import path

from attendance.views.attendance_calculate_view import AttendanceCalculateView
from attendance.views.attendance_create_view import AttendanceCreateView
from attendance.views.attendance_delete_view import AttendanceDeleteView
from attendance.views.attendance_filter_view import AttendanceFilterView
from attendance.views.attendance_list_view import AttendanceListView
from attendance.views.attendance_update_view import AttendanceUpdateView

urlpatterns = [
    path("", AttendanceListView.as_view(), name="attendance_list"),
    path("filter", AttendanceFilterView.as_view(), name="attendance_filter"),
    path("<int:pk>", AttendanceListView.as_view(), name="attendance_detail"),
    path("create", AttendanceCreateView.as_view(), name="attendance_create"),
    path("<int:pk>/update", AttendanceUpdateView.as_view(), name="attendance_update"),
    path("<int:pk>/delete", AttendanceDeleteView.as_view(), name="attendance_delete"),
    path("<int:pk>/calculate", AttendanceCalculateView.as_view(), name="attendance_calculate"),
]
