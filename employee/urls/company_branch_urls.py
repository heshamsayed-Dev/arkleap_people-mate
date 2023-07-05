from django.urls import path
from employee.views.branch_api_view import CompanyBranchAPIView

urlpatterns = [
    path('', CompanyBranchAPIView.as_view(), name='branch_list'),
    path('<int:pk>', CompanyBranchAPIView.as_view(),name='branch_detail'),
    path('create', CompanyBranchAPIView.as_view(), name='branch_create'),
    path('<int:pk>/update', CompanyBranchAPIView.as_view(), name='branch_update'),
    path('<int:pk>/delete', CompanyBranchAPIView.as_view(), name='branch_delete'),

]