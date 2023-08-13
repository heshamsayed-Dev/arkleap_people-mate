from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt import views as jwt_views

from people_mate.users.api.views import UserViewSet

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("people_mate.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("employees/", include("employee.urls.employee_urls")),
    path("companies/", include("employee.urls.company_urls")),
    path("branches/", include("employee.urls.company_branch_urls")),
    path("positions/", include("employee.urls.position_urls")),
    path("departments/", include("employee.urls.department_urls")),
    path("locations/", include("employee.urls.location_urls")),
    path("policy/", include("policy.urls.policy_urls")),
    path("attendances/", include("attendance.urls.attendance_urls")),
    path("attendance-details/", include("attendance.urls.attendance_detail_urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    # path("api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login", UserViewSet.as_view({"post": "sign_in"}), name="sign_in"),
    path("api/token/refresh", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("users/create", UserViewSet.as_view({"post": "create_user"}), name="create_users"),
    path("api/signout", UserViewSet.as_view({"get": "signout"}), name="signout"),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


# admin.site.site_header = settings.ADMIN_SITE_HEADER
