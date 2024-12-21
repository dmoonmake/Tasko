# Create your views here.
import json
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Column
from task.models import Task 
from .forms import BoardForm, ColumnForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required
def board_list(request):
    # Fetch all boards where the user is a member
    user_boards = Board.objects.filter(board_members=request.user)

    # Separate boards created by the user
    boards = []
    for board in user_boards:
        boards.append({
            'board': board,
            'is_creator': board.board_created_by == request.user
        })

    return render(request, 'board/board_list.html', {'boards': boards})

def board_setting(request, board_id):
    board = get_object_or_404(Board, board_id=board_id)
    columns = board.columns.all().order_by('order')
    return render(request, 'board/board_setting.html', {'board': board, 'columns': columns})

@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            # Save the board and assign the current user as the creator
            board = form.save(commit=False)
            board.board_created_by = request.user
            board.save()
            board.board_members.set(form.cleaned_data['board_members'])
            board.board_members.add(request.user)  # Automatically add the creator to the board
            
            return redirect("board_setting", board_id=board.id)  # Redirect to the board list
    else:
        form = BoardForm()
    return render(request, 'board/board_create.html', {'form': form})

@login_required
def create_column(request, board_id):
    if request.method == "POST":
        board = get_object_or_404(Board, id=board_id)

        # Check if the board already has 6 columns
        if board.columns.count() >= 6:
            return JsonResponse({"error": "Column limit reached. You cannot add more than 8 columns."}, status=400)

        column_title = request.POST.get("column_title")
        if column_title:
            column_order = board.columns.count()  # Add the column at the end
            column = Column.objects.create(
                column_title=column_title,
                column_board=board,
                column_order=column_order
            )
            return JsonResponse({
                "id": column.id,
                "name": column.column_title,
                "order": column.column_order
            })
        else:
            return JsonResponse({"error": "Column name is required."}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required
def board_setting(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    columns = board.columns.all().order_by("column_order")  # Order by column_order
    return render(request, 'board/board_setting.html', {'board': board, 'columns': columns})

@csrf_exempt
def move_task(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task_id = data.get("task_id")
        column_id = data.get("column_id")

        task = get_object_or_404(Task, id=task_id)
        column = get_object_or_404(Column, id=column_id)

        task.task_column = column

        # Update task status based on column position
        if column.column_order == 0:
            task.task_status = "To-Do"
        elif column.column_order == column.column_board.columns.count() - 1:
            task.task_status = "Done"
        else:
            task.task_status = "In Progress"

        task.save()

        return JsonResponse({
            "message": "Task moved successfully.",
            "task_status": task.task_status,
        })

    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def reorder_columns(request, board_id):
    if request.method == "POST":
        data = json.loads(request.body)
        column_ids = data.get("column_ids")  # List of column IDs in new order
        for order, column_id in enumerate(column_ids):
            column = Column.objects.get(id=column_id)
            column.column_order = order
            column.save()
        return JsonResponse({"message": "Columns reordered successfully."})
    return JsonResponse({"error": "Invalid request method."}, status=400)

def check_board_access(user, board):
    if user not in board.board_members.all():
        raise HttpResponseForbidden("You are not authorized to access this board.")
    
@login_required
def delete_column(request, board_id, column_id):
    if request.method == "POST":
        column = get_object_or_404(Column, id=column_id, column_board__id=board_id)

        # Check if the column has tasks
        if column.tasks.exists():  # Assuming the related name for tasks in the Column model is "tasks"
            return JsonResponse({"success": False, "error": "Cannot delete column with existing tasks."}, status=400)

        # Delete the column
        column.delete()

        # Fetch the updated column list
        updated_columns = Column.objects.filter(column_board_id=board_id).values("id", "column_title")
        return JsonResponse({"success": True, "message": "Column deleted successfully."})

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

@login_required
def board_display(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    columns = board.columns.all().order_by("column_order")
    tasks = Task.objects.filter(task_column__in=columns)  # Fetch tasks in the board's columns
    # Check if the logged-in user is the creator of the board
    is_creator = board.board_created_by == request.user
    
    return render(request, 'board/board_display.html', {'board': board, 'columns': columns, 'tasks': tasks})

@login_required
def delete_board(request, board_id):
    if request.method == "POST":
        board = get_object_or_404(Board, id=board_id)

        # Only the board creator can delete the board
        if board.board_created_by != request.user:
            return JsonResponse({"error": "You do not have permission to delete this board."}, status=403)

        board.delete()
        # Redirect to the Board List page
        return redirect('board_list')  # Use the name of the board list URL
    return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required
def add_task_to_column(request, column_id): #Fetch and display task to column
    if request.method == "POST":
        column = get_object_or_404(Column, id=column_id)
        board = column.column_board

        task_title = request.POST.get("task_title")
        assigned_to_id = request.POST.get("assigned_to")  # Optional
        assigned_to = None

        if assigned_to_id:
            assigned_to = board.board_members.filter(id=assigned_to_id).first()

        # Determine task status based on the column's position
        if column.column_order == 0:
            task_status = "To-Do"
        elif column.column_order == board.columns.count() - 1:
            task_status = "Done"
        else:
            task_status = "In Progress"

        # Create the task
        task = Task.objects.create(
            task_title=task_title,
            task_status=task_status,
            task_column=column,
            task_assigned_to=assigned_to,
        )

        return JsonResponse({
            "message": "Task added successfully.",
            "task_id": task.id,
            "task_title": task.task_title,
            "task_status": task.task_status,
            "assigned_to": assigned_to.username if assigned_to else None,
        })
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
@login_required
def move_task(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task_id = data.get("task_id")
        column_id = data.get("column_id")

        task = Task.objects.get(id=task_id)
        column = Column.objects.get(id=column_id)

        # Update the task's column
        task.task_column = column

        # Update the task's status based on the column's position
        if column.column_order == 0:
            task.task_status = "To-Do"
        elif column.column_order == column.column_board.columns.count() - 1:
            task.task_status = "Done"
        else:
            task.task_status = "In Progress"

        task.save()

        return JsonResponse({
            "message": "Task moved successfully.",
            "task_status": task.task_status
        })

    return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required
def create_task_in_column(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    if request.method == "POST":
        task_title = request.POST.get("task_title")
        assigned_to_id = request.POST.get("assigned_to")
        assigned_to = None

        if assigned_to_id:
            assigned_to = column.column_board.board_members.filter(id=assigned_to_id).first()

        # Determine the task status based on column position
        if column.column_order == 0:
            task_status = "To-Do"
        elif column.column_order == column.column_board.columns.count() - 1:
            task_status = "Done"
        else:
            task_status = "In Progress"

        task = Task.objects.create(
            task_title=task_title,
            task_status=task_status,
            task_column=column,
            task_assigned_to=assigned_to
        )

        return JsonResponse({
            "message": "Task added successfully.",
            "task_id": task.id,
            "task_title": task.task_title,
            "task_status": task.task_status,
            "assigned_to": assigned_to.username if assigned_to else "Unassigned"
        })

    return JsonResponse({"error": "Invalid request method."}, status=400)

