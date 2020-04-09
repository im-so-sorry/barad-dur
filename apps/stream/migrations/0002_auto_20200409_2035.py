# Generated by Django 2.2.5 on 2020-04-09 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stream", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="stream",
            name="description",
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name="stream",
            name="service",
            field=models.CharField(
                choices=[("vk", "vk.com"), ("twitter", "twitter.com")], max_length=64, null=True
            ),
        ),
    ]