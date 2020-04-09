import uuid

from django.conf import settings
from django.utils.translation import gettext_lazy as _


def get_token():
    return str(uuid.uuid4())


def get_user_token(username: str):
    return uuid.uuid5(settings.UUID_NAMESPACE, username)


def check_username_exists(username: str):
    from apps.user.models import User

    return User.objects.filter(username=username).exists()


def get_self_or_user(pk, self_user=None):
    from apps.user.models import User

    if self_user is not None and not (self_user.is_staff or self_user.is_superuser):
        return self_user
    user = User.objects.filter(pk=pk).first()
    return user or self_user


def send_password_reset_mail(user):
    raise NotImplementedError
