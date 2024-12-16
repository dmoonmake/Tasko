from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['task_title', 'task_description', 'task_status', 'task_priority', 'task_deadline', 'task_assigned_to']
    widgets = {
      'task_assigned_to': forms.Select(attrs={'class': 'form-control'}),
      'task_deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    }
