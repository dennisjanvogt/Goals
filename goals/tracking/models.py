# tracking/models.py
from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):

    KATEGORIEN = [
        ('Gesundheit', 'Gesundheit'),
        ('Finanzen', 'Finanzen'),
        ('Karriere', 'Karriere')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    definition = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    ziel_wert = models.IntegerField()
    fortschritt = models.FloatField()
    einheit = models.CharField(max_length=20)
    start = models.DateField()
    end = models.DateField()
    kategorie = models.CharField(choices=KATEGORIEN)

    def __str__(self):
        return f"{self.definition}"