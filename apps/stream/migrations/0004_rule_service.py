# Generated by Django 2.2.5 on 2020-04-26 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0003_auto_20200426_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='service',
            field=models.CharField(choices=[('vk', 'vk.com'), ('twitter', 'twitter.com')], max_length=64, null=True),
        ),
    ]