# Generated by Django 2.2.5 on 2020-04-26 16:25

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0004_rule_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('service', models.CharField(choices=[('vk', 'vk.com'), ('twitter', 'twitter.com')], max_length=64, null=True)),
                ('event_type', models.CharField(max_length=64, null=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), blank=True, default=list, size=None)),
                ('payload', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True, verbose_name='Additional data')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]