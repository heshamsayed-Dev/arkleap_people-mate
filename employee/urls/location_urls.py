from django.urls import path

from employee.views.location_create_view import LocationCreateView
from employee.views.location_delete_view import LocationDeleteView
from employee.views.location_list_view import LocationListView
from employee.views.location_update_view import LocationUpdateView

urlpatterns = [
    path("", LocationListView.as_view(), name="location_list"),
    path("<int:pk>", LocationListView.as_view(), name="location_detail"),
    path("create", LocationCreateView.as_view(), name="location_create"),
    path("<int:pk>/update", LocationUpdateView.as_view(), name="location_update"),
    path("<int:pk>/delete", LocationDeleteView.as_view(), name="location_delete"),
]
