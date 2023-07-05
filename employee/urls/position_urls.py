from django.urls import path

from employee.views.position_create_view import PositionCreateView
from employee.views.position_delete_view import PositionDeleteView
from employee.views.position_list_view import PositionListView
from employee.views.position_update_view import PositionUpdateView

urlpatterns = [
    path("", PositionListView.as_view(), name="position_list"),
    path("<int:pk>", PositionListView.as_view(), name="position_detail"),
    path("create", PositionCreateView.as_view(), name="position_create"),
    path("<int:pk>/update", PositionUpdateView.as_view(), name="position_update"),
    path("<int:pk>/delete", PositionDeleteView.as_view(), name="position_delete"),
]
