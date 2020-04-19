from rest_framework.routers import DefaultRouter

from apps.user.views import SocialUserModelView

router = DefaultRouter()

router.register("social_user", SocialUserModelView)

urlpatterns = [
]

urlpatterns += router.urls
