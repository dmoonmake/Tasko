# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Task List View
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task/task_list.html', {'tasks': tasks})

def task_list_table(request):
    tasks = Task.objects.all()
    return render(request, 'task/task_list_Table.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to task list after creating
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task/task_create.html', {'form': form})

def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')  # Redirect to task list after deleting

def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task/task_edit.html', {'form': form, 'task': task})

# Task Detail View
def task_detail(request, task_id):
    # Retrieve the task by its ID or show 404 if not found
    task = get_object_or_404(Task, id=task_id)
    
    # Return task details as JSON
    return JsonResponse({
        'task_title': task.task_title,
        'task_description': task.task_description,
        'task_status': task.task_status,
        'task_priority': task.task_priority,
        'task_created_at': task.task_created_at.strftime('%Y-%m-%d %H:%M:%S'),
    })

@csrf_exempt
def update_task_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('id')
        new_status = data.get('status')

        try:
            task = Task.objects.get(id=task_id)
            if new_status == 'todo':
                task.task_status = 'To-Do'
            elif new_status == 'inprogress':
                task.task_status = 'In Progress'
            elif new_status == 'done':
                task.task_status = 'Done'
            task.save()
            return JsonResponse({'message': 'Task status updated successfully.'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

