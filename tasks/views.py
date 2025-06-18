from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from django.utils import timezone

@login_required
def task_list(request):
    status_filter = request.GET.get('status')
    ordering = request.GET.get('ordering', 'due_date')

    tasks = Task.objects.filter(user=request.user)
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    tasks = tasks.order_by(ordering)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status', 'new')
        due_date = request.POST.get('due_date')

        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            status=status,
            due_date=due_date
        )
        return redirect('task_list')

    return render(request, 'tasks/task_form.html')

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.due_date = request.POST.get('due_date')
        task.save()
        return redirect('task_list')

    return render(request, 'tasks/task_form.html', {'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
