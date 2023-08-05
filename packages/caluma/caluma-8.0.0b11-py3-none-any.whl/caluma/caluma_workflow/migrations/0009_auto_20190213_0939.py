# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-13 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("caluma_workflow", "0008_auto_20190208_1302")]

    operations = [
        migrations.AddField(
            model_name="case",
            name="closed_at",
            field=models.DateTimeField(
                blank=True,
                help_text="Time when case has either been canceled or completed",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="closed_by_group",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="case",
            name="closed_by_user",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="workitem",
            name="closed_at",
            field=models.DateTimeField(
                blank=True,
                help_text="Time when work item has either been canceled or completed",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="workitem",
            name="closed_by_group",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="workitem",
            name="closed_by_user",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
