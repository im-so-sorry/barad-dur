from django.contrib import admin

from apps.social.models import NotificationService


@admin.register(NotificationService)
class NotificationServiceAdmin(admin.ModelAdmin):
    pass
