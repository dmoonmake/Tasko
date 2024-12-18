from django.urls import path
from . import views  # Import views from the same app
# from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.task_list, name='task_list'),  # Default route to the task list view
    path('table/', views.task_list_table, name='task_list_table'),
    path('create/', views.task_create, name='task_create'),
    path('edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('update-status/', views.update_task_status, name='update_task_status'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/detail/', views.task_detail_ajax, name='task_detail_ajax'),

    # # Login, Logout, and Register
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('accounts/register/', views.register, name='register'),
]
