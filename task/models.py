
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Task(models.Model):
  STATUS_CHOICES = [
    ("To-Do", "To-Do"),
    ("In Progress", "In Progress"),
    ("Done", "Done"),
  ]

  # Task priority options
  PRIORITY_CHOICES = [
    ("Low", "Low"),
    ("Medium", "Medium"),
    ("High", "High"),
  ]
  task_title = models.CharField(max_length=255, verbose_name="Title")  
  task_description = models.TextField(blank=True, null=True, verbose_name="Description")  
  task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="To-Do")
  task_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Medium", verbose_name="Priority")  
  task_assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="assigned_tasks", verbose_name="Assigned To")
  task_created_at = models.DateTimeField(auto_now_add=True)  
  task_updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
  task_deadline = models.DateField(blank=True, null=True, verbose_name="Deadline")
  task_closed_at = models.DateTimeField(null=True, blank=True) # Track close date
  task_column = models.ForeignKey('board.Column', on_delete=models.CASCADE, null=True, blank=True, related_name="tasks")

class Meta:
  ordering = ["-task_priority", "task_status", "task_created_at"]
  verbose_name = "Task"
  verbose_name_plural = "Tasks"

def __str__(self):
  return self.task_title

def save(self, *args, **kwargs):
    # Automatically update task_closed_at when task_status is "Done"
    if self.task_status == "Done" and not self.task_closed_at:
      self.task_closed_at = now()
    elif self.task_status != "Done" and self.task_closed_at:
      self.task_closed_at = None  # Clear the closed_at field if the status is changed from "Done"
    
    if self.task_column:
      if self.task_column.column_order == 0:  # Leftmost column
        self.task_status = "To-Do"
      elif self.task_column.column_order == self.task_column.column_board.columns.count() - 1:  # Rightmost column
        self.task_status = "Done"
      else:
        self.task_status = "In Progress"
    super().save(*args, **kwargs)

def is_overdue(self):
  """Check if the task deadline has passed and the task is not closed."""
  if self.task_deadline and not self.task_closed_at:
    return self.task_deadline < now()
  return False
