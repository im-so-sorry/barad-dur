from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as ParentUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


@admin.register(User)
class UserAdmin(ParentUserAdmin):
    readonly_fields = ("date_joined",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
