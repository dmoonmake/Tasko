# Generated by Django 5.1.4 on 2024-12-16 21:42

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
            name="Board",
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
                (
                    "board_title",
                    models.CharField(max_length=255, verbose_name="Board Title"),
                ),
                (
                    "board_description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "board_users",
                    models.ManyToManyField(
                        related_name="boards",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Users",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Column",
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
                (
                    "column_title",
                    models.CharField(max_length=255, verbose_name="Column Title"),
                ),
                ("column_order", models.PositiveIntegerField(default=0)),
                (
                    "column_board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="columns",
                        to="board.board",
                    ),
                ),
            ],
        ),
    ]
