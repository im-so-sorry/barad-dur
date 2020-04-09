from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.utils.choices import Choices


class NotificationService(TimeStampedModel):
    SERVICES = Choices(("vk", "vk.com"), ("telegram", "telegram.com"), ("email", "email"),)

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    service = models.CharField(max_length=64, choices=SERVICES)
    value = models.CharField(max_length=256, blank=True, null=True)

    is_active = models.BooleanField(default=False)

    verification_token = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return "{}: {} ({})".format(self.service, self.value or "", self.user.username)

    __repr__ = __str__
