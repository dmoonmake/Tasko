from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('To-Do', 'To-Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    ]

    task_title = models.CharField(max_length=200)  
    task_description = models.TextField(blank=True)  
    task_status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='To-Do'
    )  
    task_created_at = models.DateTimeField(auto_now_add=True)  
    task_closed_at = models.DateTimeField(null=True, blank=True) # Track close date

    def __str__(self):
        return self.task_title
