from typing import Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from apps.core.utils.choices import Choices
from apps.user.utils import get_token, get_user_token


class UserManager(BaseUserManager):
    def create_user(self, login, password=None, is_staff=False, is_active=True, **extra_fields):
        if not login:
            login = extra_fields.get("username")

        extra_fields.pop("username", None)
        user = self.model(username=login, is_active=is_active, is_staff=is_staff, **extra_fields)
        user.set_password(password)
        user.token = get_user_token(login)

        user.save()
        return user

    def create_superuser(self, login=None, password=None, **extra_fields):
        return self.create_user(login, password, is_staff=True, is_superuser=True, **extra_fields)

    def create_stuff(self, login=None, password=None, **extra_fields):
        return self.create_user(login, password, is_staff=True, is_superuser=False, **extra_fields)

    def staff(self):
        return self.get_queryset().filter(is_staff=True)


class User(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(max_length=256, db_index=True, unique=True, default="")
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(
        max_length=256, blank=True, null=True, default="", verbose_name=_("First Name")
    )
    last_name = models.CharField(
        max_length=256, blank=True, null=True, default="", verbose_name=_("Last name")
    )

    phone = models.CharField(max_length=32, null=True, blank=True, verbose_name=_("Phone number"))

    is_staff = models.BooleanField(default=False, verbose_name=_("Staff"))
    token = models.UUIDField(default=get_token, editable=False, unique=True, verbose_name=_("Token"))

    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    date_joined = models.DateTimeField(default=timezone.now, editable=False, verbose_name=_("Date joined"))

    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email

    def get_short_name(self):
        return self.email


class SocialUserManager(models.Manager):
    def create_user(self, username: str, service: str, user: User = None, sync_token: Optional[str] = None):
        if not user:
            other_user = SocialUser.objects.filter(sync_token=sync_token, user__isnull=False).first()
            if other_user:
                user = other_user.user
            else:
                user, _ = User.objects.get_or_create(username=f"{service}_{username}")

        social_user = SocialUser.objects.create(username=username, service=service, user=user, sync_token=sync_token)

        return social_user

    def get_or_create_user(self, username: str, service: str, sync_token: Optional[str] = None):
        social_user = SocialUser.objects.filter(username=username, service=service).first()
        return social_user or self.create_user(username, service, sync_token=sync_token)


class SocialUser(models.Model):
    SERVICES = Choices(
        ("vk", "vk.com"),
        ("tg", "telegram.com"),
        ("service", "service")
    )

    username = models.CharField(max_length=256, db_index=True, unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sync_token = models.CharField(max_length=64, null=True, blank=True)
    service = models.CharField(max_length=256, choices=SERVICES)

    objects = SocialUserManager()
