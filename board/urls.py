from django.urls import path
from . import views

urlpatterns = [
    path('', views.board_list, name='board_list'),
    path('<int:board_id>/', views.board_detail, name='board_detail'),
    path('<int:board_id>/create-column/', views.create_column, name='create_column'),
    path('create/', views.create_board, name='create_board'),
]

