# Generated by Django 2.2.6 on 2019-10-25 09:50

import uuid

import django.db.models.deletion
import localized_fields.fields.field
import simple_history.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("caluma_form", "0024_auto_20190919_1244")]

    operations = [
        migrations.CreateModel(
            name="HistoricalDynamicOption",
            fields=[
                ("created_at", models.DateTimeField(blank=True, editable=False)),
                ("modified_at", models.DateTimeField(blank=True, editable=False)),
                (
                    "created_by_user",
                    models.CharField(blank=True, max_length=150, null=True),
                ),
                (
                    "created_by_group",
                    models.CharField(
                        blank=True, db_index=True, max_length=150, null=True
                    ),
                ),
                ("history_user_id", models.CharField(max_length=150, null=True)),
                (
                    "id",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                ("value", models.CharField(blank=True, max_length=255, null=True)),
                ("label", localized_fields.fields.field.LocalizedField(required=[])),
                (
                    "history_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "document",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="caluma_form.Document",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="caluma_form.Question",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical dynamic option",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="DynamicOption",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by_user",
                    models.CharField(blank=True, max_length=150, null=True),
                ),
                (
                    "created_by_group",
                    models.CharField(
                        blank=True, db_index=True, max_length=150, null=True
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("value", models.CharField(blank=True, max_length=255, null=True)),
                ("label", localized_fields.fields.field.LocalizedField(required=[])),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="caluma_form.Document",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="caluma_form.Question",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]
