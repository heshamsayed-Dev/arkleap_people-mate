from rest_framework.routers import DefaultRouter

from policy.views.policy_api_view import PolicyViewSet

app_name = "policy"

router = DefaultRouter()
router.register("", PolicyViewSet, basename="policy")

urlpatterns = router.urls
urlpatterns = [
    *router.urls,
]
