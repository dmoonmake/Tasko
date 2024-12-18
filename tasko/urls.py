"""
URL configuration for tasko project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from task import views
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from tasko import views as tasko_views  # Custom registration view
from . import views  # Import your custom views
from task import views as task_views  # Import from 'task' app, not 'tasko'

def home(request):
    return HttpResponse('<h1>Welcome to Tasko!</h1><p>Go to <a href="/tasks/">Task List</a>.</p>')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('task.urls')),  # Include task app URLs
    # path('tasks/', task_views.task_list, name='task_list'),  # Use the correct path
    path('boards/', include('board.urls')),
    path('', home),  # Custom view for root URL
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', tasko_views.register, name='register'),  # Add this for registration
]

