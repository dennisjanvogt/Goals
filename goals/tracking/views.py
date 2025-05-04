# tracking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, F, ExpressionWrapper, FloatField, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Goal
from .forms import GoalForm

@login_required
def goals_view(request):
    today = timezone.now().date()
    
    # Filter goals by the authenticated user, showing only parent goals by default
    parent_goals = Goal.objects.filter(user=request.user, parent__isnull=True)
    
    # Get subtasks if a parent_id is provided in the URL
    selected_goal_id = request.GET.get('parent_id')
    selected_goal = None
    subtasks = None
    
    if selected_goal_id:
        try:
            selected_goal = Goal.objects.get(id=selected_goal_id, user=request.user)
            subtasks = Goal.objects.filter(parent=selected_goal)
        except Goal.DoesNotExist:
            pass
    
    # Fortschritt in Prozent für jedes Ziel berechnen
    parent_goals_with_progress = parent_goals.annotate(
        progress_percent=ExpressionWrapper(
            (F('fortschritt') * 100.0) / F('ziel_wert'), 
            output_field=FloatField()
        )
    )
    
    if subtasks:
        subtasks = subtasks.annotate(
            progress_percent=ExpressionWrapper(
                (F('fortschritt') * 100.0) / F('ziel_wert'), 
                output_field=FloatField()
            )
        )
    
    # Durchschnittlichen Fortschritt berechnen
    avg_progress = parent_goals_with_progress.aggregate(avg=Avg('progress_percent'))['avg'] or 0
    
    # Aktive Ziele (nicht abgelaufen)
    active_goals = parent_goals.filter(end__gte=today).count()
    
    # Nächstes Fälligkeitsdatum
    nearest_deadline_goal = parent_goals.filter(end__gte=today).order_by('end').first()
    nearest_deadline = nearest_deadline_goal.end if nearest_deadline_goal else None
    
    context = {
        'goals': parent_goals_with_progress,
        'avg_progress': avg_progress,
        'active_goals': active_goals,
        'nearest_deadline': nearest_deadline,
        'today': today,
        'selected_goal': selected_goal,
        'subtasks': subtasks,
    }
    
    return render(request, 'tracking/home.html', context)

@login_required
def add_goal(request):
    parent_id = request.GET.get('parent_id')
    parent_goal = None
    
    if parent_id:
        parent_goal = get_object_or_404(Goal, id=parent_id, user=request.user)
    
    if request.method == 'POST':
        form = GoalForm(request.POST, user=request.user)
        if form.is_valid():
            # Set the user before saving
            goal = form.save(commit=False)
            goal.user = request.user
            
            # Handle parent relationship
            if 'parent' in form.cleaned_data and form.cleaned_data['parent']:
                goal.parent = form.cleaned_data['parent']
                
                # Update parent's fortschritt if auto_calculate is True
                parent = goal.parent
                if parent and parent.auto_calculate:
                    parent.save()  # Das wird die get_fortschritt_from_subtasks-Methode aufrufen
            
            goal.save()
            messages.success(request, 'Ziel erfolgreich erstellt!')
            
            # Redirect back to parent if this was a subtask creation
            if parent_goal:
                return redirect(f'{reverse("goals")}?parent_id={parent_goal.id}')
            return redirect('goals')
    else:
        # Set today's date as default for start field for new goals
        initial_data = {'start': timezone.now().date()}
        if parent_goal:
            # Wenn Unterziel erstellt wird, verwende die Kategorie des Elternziels
            initial_data['kategorie'] = parent_goal.kategorie
            initial_data['parent'] = parent_goal
            
        form = GoalForm(initial=initial_data, user=request.user)
    
    return render(request, 'tracking/add_update_goal.html', {
        'form': form,
        'title': 'Neues Ziel erstellen',
        'button_text': 'Erstellen',
        'parent_goal': parent_goal
    })

@login_required
def update_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    had_auto_calculate = goal.auto_calculate
    
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal, user=request.user)
        if form.is_valid():
            goal = form.save()
            
            # Wenn auto_calculate geändert wurde, oder es bereits aktiviert war,
            # aktualisiere den Fortschritt
            if form.cleaned_data['auto_calculate'] or had_auto_calculate:
                goal.fortschritt = goal.get_fortschritt_from_subtasks()
                goal.save()
                
            messages.success(request, 'Ziel erfolgreich aktualisiert!')
            
            # Redirect back to parent if this is a subtask
            if goal.parent:
                return redirect(f'{reverse("goals")}?parent_id={goal.parent.id}')
            return redirect('goals')
    else:
        # Make sure to preserve the date values by passing the instance to the form
        form = GoalForm(instance=goal, user=request.user)
    
    return render(request, 'tracking/add_update_goal.html', {
        'form': form,
        'title': 'Ziel bearbeiten',
        'button_text': 'Speichern',
        'goal': goal
    })

@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    parent = goal.parent
    
    if request.method == 'POST':
        goal.delete()
        
        # Update parent's progress if auto_calculate is enabled
        if parent and parent.auto_calculate:
            parent.fortschritt = parent.get_fortschritt_from_subtasks()
            parent.save()
            
        messages.success(request, 'Ziel erfolgreich gelöscht!')
        
        # Redirect back to parent if this was a subtask
        if parent:
            return redirect(f'{reverse("goals")}?parent_id={parent.id}')
        return redirect('goals')
    
    return render(request, 'tracking/delete_goal.html', {'goal': goal})

@login_required
def update_progress(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    
    # Verhindere Aktualisierung, wenn auto_calculate aktiviert ist
    if goal.auto_calculate:
        messages.warning(request, 'Dieses Ziel wird automatisch berechnet und kann nicht manuell aktualisiert werden.')
        
        # Redirect back to parent if this is a subtask
        if goal.parent:
            return redirect(f'{reverse("goals")}?parent_id={goal.parent.id}')
        return redirect('goals')
    
    if request.method == 'POST':
        new_progress = request.POST.get('fortschritt')
        if new_progress:
            try:
                new_progress = float(new_progress)
                if new_progress <= goal.ziel_wert:
                    old_progress = goal.fortschritt
                    goal.fortschritt = new_progress
                    goal.save()
                    
                    # Aktualisiere übergeordnetes Ziel, falls vorhanden und auto_calculate ist True
                    if goal.parent and goal.parent.auto_calculate:
                        parent = goal.parent
                        parent.fortschritt = parent.get_fortschritt_from_subtasks()
                        parent.save()
                    
                    messages.success(request, 'Fortschritt aktualisiert!')
                else:
                    messages.error(request, 'Der Fortschritt kann nicht größer als der Zielwert sein.')
            except ValueError:
                messages.error(request, 'Bitte geben Sie einen gültigen Wert ein.')
    
    # Redirect back to parent if this is a subtask
    if goal.parent:
        return redirect(f'{reverse("goals")}?parent_id={goal.parent.id}')
    return redirect('goals')