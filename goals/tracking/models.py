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





class YearlyGoal(models.Model):
    YEARS_CHOICES = [
        (2020, '2020'),
        (2021, '2021'),
        (2022, '2022'),
        (2023, '2023'),
        (2024, '2024'),
        (2025, '2025'),
        (2026, '2026'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='yearly_goals')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    year = models.IntegerField(choices=YEARS_CHOICES, default=2025)
    start_value = models.FloatField()
    target_value = models.FloatField()
    unit = models.CharField(max_length=50)
    
    # Monthly values
    january = models.FloatField(null=True, blank=True)
    february = models.FloatField(null=True, blank=True)
    march = models.FloatField(null=True, blank=True)
    april = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    june = models.FloatField(null=True, blank=True)
    july = models.FloatField(null=True, blank=True)
    august = models.FloatField(null=True, blank=True)
    september = models.FloatField(null=True, blank=True)
    october = models.FloatField(null=True, blank=True)
    november = models.FloatField(null=True, blank=True)
    december = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
    
    def get_current_value(self):
        """Returns the most recent non-null monthly value"""
        months = [
            self.december, self.november, self.october, 
            self.september, self.august, self.july,
            self.june, self.may, self.april, 
            self.march, self.february, self.january
        ]
        
        for value in months:
            if value is not None:
                return value
        
        return self.start_value
    
    def get_progress_percentage(self):
        """Calculate progress percentage towards target"""
        current = self.get_current_value()
        target_diff = self.target_value - self.start_value
        
        if target_diff == 0:  # Avoid division by zero
            return 100 if current >= self.target_value else 0
            
        current_diff = current - self.start_value
        percentage = (current_diff / target_diff) * 100
        
        # Cap percentage between 0 and 100
        return max(0, min(100, percentage))
    
    def get_monthly_values(self):
        """Returns all monthly values as a list"""
        return [
            ('Januar', self.january),
            ('Februar', self.february),
            ('März', self.march),
            ('April', self.april),
            ('Mai', self.may),
            ('Juni', self.june),
            ('Juli', self.july),
            ('August', self.august),
            ('September', self.september),
            ('Oktober', self.october),
            ('November', self.november),
            ('Dezember', self.december)
        ]