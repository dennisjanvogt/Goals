from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, F, ExpressionWrapper, FloatField
from .models import Goal

def goals_view(request):
    today = timezone.now().date()
    
    # Alle Ziele abrufen
    goals = Goal.objects.all()
    
    # Durchschnittlichen Fortschritt berechnen
    avg_progress = goals.annotate(
        progress_percent=ExpressionWrapper(
            (F('fortschritt') * 100.0) / F('ziel_wert'), 
            output_field=FloatField()
        )
    ).aggregate(avg=Avg('progress_percent'))['avg'] or 0
    
    # Aktive Ziele (nicht abgelaufen)
    active_goals = goals.filter(end__gte=today).count()
    
    # Nächstes Fälligkeitsdatum
    nearest_deadline_goal = goals.filter(end__gte=today).order_by('end').first()
    nearest_deadline = nearest_deadline_goal.end if nearest_deadline_goal else None
    
    context = {
        'goals': goals,
        'avg_progress': avg_progress,
        'active_goals': active_goals,
        'nearest_deadline': nearest_deadline,
        'today': today,
    }
    
    return render(request, 'tracking/home.html', context)