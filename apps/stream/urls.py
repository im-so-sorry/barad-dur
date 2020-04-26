from rest_framework.routers import DefaultRouter

from apps.stream.views import StreamModelView, RuleModelView, EventViewSet

router = DefaultRouter()

router.register("stream", StreamModelView)
router.register("rule", RuleModelView)
router.register("event", EventViewSet)

urlpatterns = [
]

urlpatterns += router.urls
