from django.db import models


class Project(models.Model):
    name = models.SlugField(max_length=128)
    description = models.CharField(max_length=512)

    owner = models.ForeignKey("user.User", on_delete=models.CASCADE)
