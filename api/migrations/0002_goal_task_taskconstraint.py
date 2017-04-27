# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 10:04
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('default_location', models.CharField(blank=True, max_length=500, null=True)),
                ('default_priority', models.PositiveIntegerField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('parent_goal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Goal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task_type', models.PositiveSmallIntegerField(choices=[(0, 'Fixed Event'), (1, 'Flexible'), (2, 'One-Shot')])),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('priority', models.PositiveIntegerField()),
                ('total_time_required_m', models.PositiveIntegerField(blank=True, null=True)),
                ('completion_verification_required', models.BooleanField(default=True)),
                ('completed', models.BooleanField(default=False)),
                ('parent_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Goal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskConstraint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('constraint_type', models.PositiveSmallIntegerField(choices=[(0, 'Min TA Interval Duration (m)'), (1, 'Max TA Interval Duration (m)'), (2, 'Day Restriction'), (4, 'Reoccurring'), (5, 'Task Dependency'), (6, 'Earliest Start Time'), (7, 'Latest End Time')])),
                ('settings', django.contrib.postgres.fields.jsonb.JSONField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Task')),
            ],
        ),
    ]