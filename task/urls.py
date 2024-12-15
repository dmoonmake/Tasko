from django.urls import path
from . import views  # Import views from the same app

urlpatterns = [
    path('', views.task_list, name='task_list'),  # Default route to the task list view
]
