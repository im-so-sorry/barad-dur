from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.core.models import TimeStampedModel
from apps.core.utils.choices import Choices
from apps.stream import tasks

SERVICES = Choices(("vk", "vk.com"), ("twitter", "twitter.com"), )


class Stream(TimeStampedModel):
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE)
    service = models.CharField(max_length=64, null=True, choices=SERVICES)

    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.service, self.project)

    __repr__ = __str__


class Rule(TimeStampedModel):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="rules")
    service = models.CharField(max_length=64, null=True, choices=SERVICES)

    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

    def __str__(self):
        return "{} - {}".format(self.key, self.value)

    __repr__ = __str__


class Event(TimeStampedModel):
    service = models.CharField(max_length=64, null=True, choices=SERVICES)

    event_type = models.CharField(max_length=64, null=True)

    tags = ArrayField(models.CharField(max_length=64), blank=True, default=list)

    payload = JSONField(default=dict, null=True, blank=True, verbose_name="Additional data")

    class Meta:
        ordering = ("created",)


@receiver(post_delete, sender=Rule)
def create_add_rule(sender, instance, *args, **kwargs):
    tasks.remove_rule(instance.key)
