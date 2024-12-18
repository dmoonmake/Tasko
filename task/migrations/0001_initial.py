# Generated by Django 5.1.4 on 2024-12-16 20:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task_title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "task_description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "task_status",
                    models.CharField(
                        choices=[
                            ("To-Do", "To-Do"),
                            ("In Progress", "In Progress"),
                            ("Done", "Done"),
                        ],
                        default="To-Do",
                        max_length=20,
                    ),
                ),
                (
                    "task_priority",
                    models.CharField(
                        choices=[
                            ("Low", "Low"),
                            ("Medium", "Medium"),
                            ("High", "High"),
                        ],
                        default="Medium",
                        max_length=20,
                        verbose_name="Priority",
                    ),
                ),
                ("task_created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "task_updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Last Updated"),
                ),
                (
                    "task_deadline",
                    models.DateField(blank=True, null=True, verbose_name="Deadline"),
                ),
                ("task_closed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "task_assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_tasks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Assigned To",
                    ),
                ),
            ],
        ),
    ]
