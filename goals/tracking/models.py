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
    
    # Neues Feld für aktuellen Stand
    current_value = models.FloatField(null=True, blank=True, 
                                      help_text="Aktueller Stand unabhängig von monatlichen Werten")
    
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
        """Returns either the explicitly set current value or the most recent non-null monthly value"""
        # Wenn ein expliziter aktueller Wert gesetzt ist, diesen zurückgeben
        if self.current_value is not None:
            return self.current_value
            
        # Sonst wie bisher den letzten monatlichen Wert zurückgeben
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
        """Calculate progress percentage towards target with improved handling of edge cases"""
        current = self.get_current_value()
        target_diff = self.target_value - self.start_value
        
        # Wenn Start- und Zielwert identisch sind, prüfe ob das Ziel erreicht wurde
        if target_diff == 0:
            return 100 if current >= self.target_value else 0
            
        # Wenn das Ziel ist, einen Wert zu reduzieren (z.B. Gewicht verlieren)
        if self.target_value < self.start_value:
            # Umgekehrte Berechnung für Reduktionsziele
            current_diff = self.start_value - current
            max_diff = self.start_value - self.target_value
            percentage = (current_diff / max_diff) * 100 if max_diff != 0 else 0
        else:
            # Normale Berechnung für Wachstumsziele
            current_diff = current - self.start_value
            percentage = (current_diff / target_diff) * 100
        
        # Prozentsatz zwischen 0 und 100 begrenzen
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