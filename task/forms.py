from django import forms
from .models import Task
from django.utils import timezone

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['task_title', 'task_description', 'task_status', 'task_priority', 'task_deadline', 'task_assigned_to']
    widgets = {
      'task_assigned_to': forms.Select(attrs={'class': 'form-control'}),
      'task_deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    }

  def clean_task_deadline(self):
    deadline = self.cleaned_data.get('task_deadline')
    if deadline and deadline < timezone.now().date():
      raise forms.ValidationError("Deadline cannot be in the past.")
    return deadline
