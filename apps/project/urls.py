from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from apps.project.views import ProjectModelView

router = DefaultRouter()

router.register("project", ProjectModelView)

urlpatterns = [
]

urlpatterns += router.urls
