from django.urls import path
from employee.views.company_api_view import CompanyAPIView

urlpatterns = [
    path('', CompanyAPIView.as_view(), name='company_list'),
    path('<int:pk>', CompanyAPIView.as_view(),name='company_detail'),
    path('create', CompanyAPIView.as_view(), name='company_create'),
    path('<int:pk>/update', CompanyAPIView.as_view(), name='company_update'),
    path('<int:pk>/delete', CompanyAPIView.as_view(), name='company_delete'),
]