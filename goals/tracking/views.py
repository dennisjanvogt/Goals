from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, F, ExpressionWrapper, FloatField
from .models import Goal
from .forms import GoalForm
from django.contrib import messages

def goals_view(request):
    today = timezone.now().date()
    
    # Alle Ziele abrufen
    goals = Goal.objects.all()
    
    # Fortschritt in Prozent für jedes Ziel berechnen
    # Verwenden von F() expressions für die Berechnung im Datenbankquery
    goals_with_progress = goals.annotate(
        progress_percent=ExpressionWrapper(
            (F('fortschritt') * 100.0) / F('ziel_wert'), 
            output_field=FloatField()
        )
    )
    
    # Durchschnittlichen Fortschritt berechnen
    avg_progress = goals_with_progress.aggregate(avg=Avg('progress_percent'))['avg'] or 0
    
    # Aktive Ziele (nicht abgelaufen)
    active_goals = goals.filter(end__gte=today).count()
    
    # Nächstes Fälligkeitsdatum
    nearest_deadline_goal = goals.filter(end__gte=today).order_by('end').first()
    nearest_deadline = nearest_deadline_goal.end if nearest_deadline_goal else None
    
    context = {
        'goals': goals_with_progress,
        'avg_progress': avg_progress,
        'active_goals': active_goals,
        'nearest_deadline': nearest_deadline,
        'today': today,
    }
    
    return render(request, 'tracking/home.html', context)

def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ziel erfolgreich erstellt!')
            return redirect('goals')
    else:
        # Initialisiere Formular mit heutigem Datum als Startdatum
        form = GoalForm(initial={'start': timezone.now().date()})
    
    return render(request, 'tracking/add_update_goal.html', {
        'form': form,
        'title': 'Neues Ziel erstellen',
        'button_text': 'Erstellen'
    })

def update_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ziel erfolgreich aktualisiert!')
            return redirect('goals')
    else:
        form = GoalForm(instance=goal)
    
    return render(request, 'tracking/add_update_goal.html', {
        'form': form,
        'title': 'Ziel bearbeiten',
        'button_text': 'Speichern',
        'goal': goal
    })

def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Ziel erfolgreich gelöscht!')
        return redirect('goals')
    
    return render(request, 'tracking/delete_goal.html', {'goal': goal})

def update_progress(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    
    if request.method == 'POST':
        new_progress = request.POST.get('fortschritt')
        if new_progress:
            try:
                new_progress = float(new_progress)
                if new_progress <= goal.ziel_wert:
                    goal.fortschritt = new_progress
                    goal.save()
                    messages.success(request, 'Fortschritt aktualisiert!')
                else:
                    messages.error(request, 'Der Fortschritt kann nicht größer als der Zielwert sein.')
            except ValueError:
                messages.error(request, 'Bitte geben Sie einen gültigen Wert ein.')
                
    return redirect('goals')