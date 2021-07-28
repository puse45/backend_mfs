# Generated by Django 3.2.5 on 2021-07-28 13:38

import uuid

import django.contrib.postgres.fields
from django.db import migrations, models

import pointer.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ClosestPointBatchCompute",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("metadata", models.JSONField(blank=True, default=dict, null=True)),
                ("is_processing", models.BooleanField(default=True)),
                ("is_done", models.BooleanField(default=False)),
                ("csv_file", models.FileField(upload_to=pointer.models.upload_dir)),
                ("column_a", models.CharField(max_length=100)),
                ("column_b", models.CharField(max_length=100)),
                ("result", models.JSONField(default=dict)),
            ],
            options={
                "verbose_name": "Closest Point Batch Compute",
                "verbose_name_plural": "Closest Point Batch Computes",
                "ordering": ("-created_at",),
                "get_latest_by": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="ClosestPointCompute",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("metadata", models.JSONField(blank=True, default=dict, null=True)),
                ("is_processing", models.BooleanField(default=True)),
                ("is_done", models.BooleanField(default=False)),
                (
                    "points",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django.contrib.postgres.fields.ArrayField(
                            base_field=models.FloatField(), size=None
                        ),
                        size=None,
                    ),
                ),
                ("result", models.JSONField(default=dict)),
            ],
            options={
                "verbose_name": "Closest Point Compute",
                "verbose_name_plural": "Closest Point Computes",
                "ordering": ("-created_at",),
                "get_latest_by": ("-created_at",),
            },
        ),
    ]
