# tracking/models.py
from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):

    KATEGORIEN = [
        ('Gesundheit', 'Gesundheit'),
        ('Finanzen', 'Finanzen'),
        ('Karriere', 'Karriere'),
        ('Lernen', 'Lernen'),
        ('Sonstiges', 'Sonstiges')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')
    definition = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    ziel_wert = models.IntegerField()
    fortschritt = models.FloatField()
    einheit = models.CharField(max_length=20)
    start = models.DateField()
    end = models.DateField()
    kategorie = models.CharField(choices=KATEGORIEN)
    is_parent_goal = models.BooleanField(default=False)
    auto_calculate = models.BooleanField(default=False, help_text="Fortschritt automatisch aus Unterzielen berechnen")

    def __str__(self):
        return f"{self.definition}"
        
    def get_fortschritt_from_subtasks(self):
        """Berechnet den Fortschritt basierend auf Unterzielen"""
        if not self.auto_calculate:
            return self.fortschritt
            
        subtasks = self.subtasks.all()
        if not subtasks.exists():
            return self.fortschritt
            
        total_progress = 0
        total_value = 0
        
        for subtask in subtasks:
            # Fortschritt in Prozent für jedes Unterziel
            percent = subtask.fortschritt / subtask.ziel_wert
            # Gewichtung basierend auf dem Zielwert des Unterziels
            total_progress += percent * subtask.ziel_wert
            total_value += subtask.ziel_wert
            
        # Gesamtfortschritt berechnen
        if total_value > 0:
            overall_percent = total_progress / total_value
            return overall_percent * self.ziel_wert
        return 0
        
    def save(self, *args, **kwargs):
        # Falls es sich um ein übergeordnetes Ziel handelt mit Auto-Berechnung,
        # aktualisiere den Fortschritt vor dem Speichern
        if self.auto_calculate and self.id:
            self.fortschritt = self.get_fortschritt_from_subtasks()
            
        super().save(*args, **kwargs)