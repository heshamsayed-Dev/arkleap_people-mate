from django.urls import path

from people_mate.users.api.views import UserViewSet
from people_mate.users.views import user_detail_view, user_redirect_view, user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("reset-password/send-email", UserViewSet.as_view({"post": "reset_password_send_email"}), name="send-email"),
    path(
        "<int:pk>/reset-password/validate-otp",
        UserViewSet.as_view({"post": "reset_password_validate_otp"}),
        name="validate-otp",
    ),
    path("<int:pk>/reset-password", UserViewSet.as_view({"post": "reset_password"}), name="reset-password"),
]
