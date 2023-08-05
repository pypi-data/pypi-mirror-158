# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-13 13:34
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("caluma_workflow", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="case",
            name="document",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="case",
                to="caluma_form.Document",
            ),
        )
    ]
