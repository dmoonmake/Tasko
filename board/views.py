# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Column
from .forms import BoardForm, ColumnForm
from django.contrib.auth.decorators import login_required

def board_list(request):
    if request.user.is_authenticated:
        boards = request.user.boards.all()  # Boards the user is a member of
    else:
        boards = []  # Empty list for unauthenticated users
    return render(request, 'board/board_list.html', {'boards': boards})

def board_detail(request, board_id):
    board = get_object_or_404(Board, board_id=board_id)
    columns = board.columns.all().order_by('order')
    return render(request, 'board/board_detail.html', {'board': board, 'columns': columns})

@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            # Save the board and assign the current user as the creator
            board = form.save(commit=False)
            board.save()
            board.users.add(request.user)  # Automatically add the creator to the board
            
            # Add additional users to the board
            additional_users = form.cleaned_data.get('users')  # Get selected users
            board.users.add(*additional_users)
            
            return redirect("board_list")  # Redirect to the board list
    else:
        form = BoardForm()
    return render(request, 'board/board_create.html', {'form': form})

def create_column(request, board_id):
    board = get_object_or_404(Board, board_id=board_id)
    if request.method == 'POST':
        form = ColumnForm(request.POST)
        if form.is_valid():
            column = form.save(commit=False)
            column.board = board
            column.save()
            return redirect('board_detail', board_id=board_id)
    else:
        form = ColumnForm()
    return render(request, 'board/column_form.html', {'form': form, 'board': board})

