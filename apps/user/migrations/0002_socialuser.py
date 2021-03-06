# Generated by Django 2.2.5 on 2020-04-19 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=256, unique=True)),
                ('sync_token', models.CharField(blank=True, max_length=64, null=True)),
                ('service', models.CharField(choices=[('vk', 'vk.com'), ('tg', 'telegram.com'), ('service', 'service')], max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
