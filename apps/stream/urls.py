from rest_framework.routers import DefaultRouter

from apps.stream.views import StreamModelView, RuleModelView

router = DefaultRouter()

router.register("stream", StreamModelView)
router.register("rule", RuleModelView)

urlpatterns = [
]

urlpatterns += router.urls
