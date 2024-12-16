# Register your models here.
from django.contrib import admin
from .models import Task

# admin.site.register(Task)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("task_title", "task_status", "task_priority", "task_assigned_to", "task_deadline", "task_closed_at")
    list_filter = ("task_status", "task_priority", "task_deadline")
    search_fields = ("task_title", "task_description")
    ordering = ("-task_created_at",)