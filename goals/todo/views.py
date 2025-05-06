from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Todo
from .forms import TodoForm
import json

@login_required
def todo_list(request):
    # Get todos for the current user
    high_priority = Todo.objects.filter(user=request.user, priority='high', completed=False)
    medium_priority = Todo.objects.filter(user=request.user, priority='medium', completed=False)
    low_priority = Todo.objects.filter(user=request.user, priority='low', completed=False)
    no_priority = Todo.objects.filter(user=request.user, priority='none', completed=False)
    completed_todos = Todo.objects.filter(user=request.user, completed=True).order_by('-created_at')[:5]
    
    context = {
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'no_priority': no_priority,
        'completed_todos': completed_todos,
    }
    
    return render(request, 'todo/todo_list.html', context)

@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Aufgabe erfolgreich hinzugefügt!')
            return redirect('todo_list')
    else:
        form = TodoForm()
    
    return render(request, 'todo/add_todo.html', {'form': form})

@login_required
def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aufgabe erfolgreich aktualisiert!')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    
    return render(request, 'todo/edit_todo.html', {'form': form, 'todo': todo})

@login_required
@require_POST
def toggle_complete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Aufgabe erfolgreich gelöscht!')
        return redirect('todo_list')
    
    return render(request, 'todo/delete_todo.html', {'todo': todo})

@login_required
@require_POST
def update_priority(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        new_priority = data.get('priority')
        
        if new_priority in [choice[0] for choice in Todo.PRIORITY_CHOICES]:
            todo.priority = new_priority
            todo.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Ungültige Priorität'}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Ungültiges JSON'}, status=400)