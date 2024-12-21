from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.board_list, name='board_list'),  # Board List page
    path('', views.board_list, name='board_list'),
    path('<int:board_id>/', views.board_setting, name='board_setting'),
    path('create/', views.create_board, name='create_board'),
    path('<int:board_id>/columns/<int:column_id>/delete/', views.delete_column, name='delete_column'),
    path('<int:board_id>/columns/reorder/', views.reorder_columns, name='reorder_columns'),
    path('<int:board_id>/display/', views.board_display, name='board_display'),
    path('<int:board_id>/settings/', views.board_setting, name='board_setting'),
    path('<int:board_id>/columns/create/', views.create_column, name='create_column'),
    path('<int:board_id>/delete/', views.delete_board, name='delete_board'),  # Delete board endpoint  # Ensure this exists
    path('<int:column_id>/add-task/', views.add_task_to_column, name='add_task_to_column'),
    path('<int:column_id>/create-task/', views.create_task_in_column, name='create_task_in_column'),
    path('move-task/', views.move_task, name='move_task'),
]

