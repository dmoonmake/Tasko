# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

# Task List View
@login_required
def task_list(request):
    messages.info(request, "Please log in to view your tasks.")
    # Filter tasks for the logged-in user
    tasks = Task.objects.filter(task_assigned_to=request.user)
    return render(request, 'task/task_list.html', {'tasks': tasks})

@login_required
def task_list_table(request):
    tasks = Task.objects.filter(task_assigned_to=request.user)
    return render(request, 'task/task_list_Table.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            # Automatically assign the task to the logged-in user
            task.task_assigned_to = request.user
            task.save()
            return redirect("task_list")  # Redirect to task list after saving
    else:
        form = TaskForm()

    return render(request, "task/task_create.html", {"form": form})


def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')  # Redirect to task list after deleting

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    referrer = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        referrer = request.POST.get('referrer', '/')
        if form.is_valid():
            form.save()
            return redirect(referrer) 
    else:
        form = TaskForm(instance=task)
        referrer = request.META.get('HTTP_REFERER', '/')
    return render(request, 'task/task_edit.html', {'form': form, 'task': task, 'referrer': referrer})

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
        'task_assigned_to': task.task_assigned_to,
        'task_deadline': task.task_deadline,
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

@login_required
def task_detail_ajax(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return JsonResponse({
        "task_id": task.id,
        "task_title": task.task_title,
        "task_description": task.task_description,
        "task_status": task.task_status,
        "task_priority": task.task_priority,
        "task_deadline": task.task_deadline.strftime("%Y-%m-%d") if task.task_deadline else None,
        "task_assigned_to": task.task_assigned_to.username if task.task_assigned_to else None,
    })