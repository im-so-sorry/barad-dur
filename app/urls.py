"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from apps.core.view import errors

admin.autodiscover()

sitemaps = dict()

urlpatterns = [
    url(r"^jet/", include("jet.urls", "jet")),
    url(r"^jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    url("^admin/", admin.site.urls),

    url("^project/", include("apps.project.urls")),
    url("^social/", include("apps.social.urls")),
    url("^stream/", include("apps.stream.urls")),

    url("^user/", include("apps.user.urls")),
]

# if settings.ADMIN_ENABLED:
urlpatterns += []
