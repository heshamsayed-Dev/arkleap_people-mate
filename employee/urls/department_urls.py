from django.urls import path

from employee.views.department_create_view import DepartmentCreateView
from employee.views.department_delete_view import DepartmentDeleteView
from employee.views.department_list_view import DepartmentListView
from employee.views.department_update_view import DepartmentUpdateView

urlpatterns = [
    path("", DepartmentListView.as_view(), name="department_list"),
    path("<int:pk>", DepartmentListView.as_view(), name="department_detail"),
    path("create", DepartmentCreateView.as_view(), name="department_create"),
    path("<int:pk>/update", DepartmentUpdateView.as_view(), name="department_update"),
    path("<int:pk>/delete", DepartmentDeleteView.as_view(), name="department_delete"),
]
