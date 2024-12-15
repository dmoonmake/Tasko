from django.urls import path
from . import views  # Import views from the same app

urlpatterns = [
    path('', views.task_list, name='task_list'),  # Default route to the task list view
    path('create/', views.task_create, name='task_create'),
    path('edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('update-status/', views.update_task_status, name='update_task_status'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
]

