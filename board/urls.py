from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.board_list, name='board_list'),  # Board List page
    path('', views.board_list, name='board_list'),
    path('<int:board_id>/', views.board_setting, name='board_setting'),
    path('create/', views.create_board, name='create_board'),
    path('<int:board_id>/columns/add/', views.create_column, name='create_column'),
    path('<int:board_id>/columns/<int:column_id>/delete/', views.delete_column, name='delete_column'),
    path('<int:board_id>/columns/reorder/', views.reorder_columns, name='reorder_columns'),
    path('<int:board_id>/display/', views.board_display, name='board_display'),
]

