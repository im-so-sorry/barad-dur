from rest_framework.routers import DefaultRouter

from apps.social.views import NotificationServiceModelView

router = DefaultRouter()

router.register("notification-service", NotificationServiceModelView)

urlpatterns = [
]

urlpatterns += router.urls
