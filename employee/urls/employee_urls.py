from django.urls import path
from employee.views import EmployeeListView, EmployeeDetailView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('<int:pk>', EmployeeDetailView.as_view(), name='employee_detail'),
    path('create', EmployeeCreateView.as_view(), name='employee_create'),
    path('<int:pk>/update', EmployeeUpdateView.as_view(), name='employee_update'),
    path('<int:pk>/delete', EmployeeDeleteView.as_view(), name='employee_delete'),
]