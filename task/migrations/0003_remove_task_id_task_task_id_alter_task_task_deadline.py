# Generated by Django 5.1.4 on 2024-12-16 18:39

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0002_task_task_assigned_to_task_task_deadline_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="id",
        ),
        migrations.AddField(
            model_name="task",
            name="task_id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="task_deadline",
            field=models.DateField(blank=True, null=True, verbose_name="Deadline"),
        ),
    ]