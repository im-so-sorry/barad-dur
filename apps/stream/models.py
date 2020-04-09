from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.utils.choices import Choices


class Stream(TimeStampedModel):
    SERVICES = Choices(("vk", "vk.com"), ("twitter", "twitter.com"),)
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE)
    service = models.CharField(max_length=64, null=True, choices=SERVICES)

    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.service, self.project)

    __repr__ = __str__


class Rule(TimeStampedModel):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name="rules")

    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

    def __str__(self):
        return "{} - {}".format(self.key, self.value)

    __repr__ = __str__
