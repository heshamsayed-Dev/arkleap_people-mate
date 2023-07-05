from rest_framework.routers import DefaultRouter

# from ..views.policie_api_view import PolicieViewSet

app_name = "policie"

router = DefaultRouter()
# router.register("", PolicieViewSet, basename="policie")

urlpatterns = router.urls
urlpatterns = [
    *router.urls,
]
