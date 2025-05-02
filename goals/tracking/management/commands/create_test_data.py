from django.core.management.base import BaseCommand
from tracking.models import Goal
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Erstellt Testdaten für die Ziel-Tracking-App'

    def handle(self, *args, **kwargs):
        # Lösche bestehende Daten
        Goal.objects.all().delete()
        
        # Aktuelles Datum
        today = timezone.now().date()
        
        # Beispieldaten
        goals_data = [
            {
                'definition': 'Laufen 100km',
                'description': 'Im Mai insgesamt 100km laufen',
                'ziel_wert': 100,
                'fortschritt': 42.5,
                'einheit': 'km',
                'start': today - timedelta(days=10),
                'end': today + timedelta(days=20),
                'kategorie': 'Gesundheit'
            },
            {
                'definition': 'Wasser trinken',
                'description': 'Täglich 2 Liter Wasser trinken',
                'ziel_wert': 60,
                'fortschritt': 45,
                'einheit': 'Liter',
                'start': today - timedelta(days=15),
                'end': today + timedelta(days=15),
                'kategorie': 'Gesundheit'
            },
            {
                'definition': 'Sparen für Urlaub',
                'description': '500€ für den Sommerurlaub sparen',
                'ziel_wert': 500,
                'fortschritt': 350,
                'einheit': '€',
                'start': today - timedelta(days=60),
                'end': today + timedelta(days=30),
                'kategorie': 'Finanzen'
            },
            {
                'definition': 'Investieren',
                'description': '1000€ in ETFs investieren',
                'ziel_wert': 1000,
                'fortschritt': 250,
                'einheit': '€',
                'start': today - timedelta(days=20),
                'end': today + timedelta(days=40),
                'kategorie': 'Finanzen'
            },
            {
                'definition': 'Django Kurs',
                'description': 'Django Onlinekurs abschließen',
                'ziel_wert': 10,
                'fortschritt': 7,
                'einheit': 'Module',
                'start': today - timedelta(days=30),
                'end': today + timedelta(days=5),
                'kategorie': 'Karriere'
            },
            {
                'definition': 'Portfolio-Projekte',
                'description': '3 Portfolio-Projekte erstellen',
                'ziel_wert': 3,
                'fortschritt': 1,
                'einheit': 'Projekte',
                'start': today - timedelta(days=45),
                'end': today + timedelta(days=60),
                'kategorie': 'Karriere'
            },
            {
                'definition': 'Bücher lesen',
                'description': '12 Bücher in 2025 lesen',
                'ziel_wert': 12,
                'fortschritt': 5,
                'einheit': 'Bücher',
                'start': today - timedelta(days=120),
                'end': today + timedelta(days=150),
                'kategorie': 'Karriere'
            },
            {
                'definition': 'Outdoorsport',
                'description': '30 Tage Sport im Freien machen',
                'ziel_wert': 30,
                'fortschritt': 8,
                'einheit': 'Tage',
                'start': today - timedelta(days=25),
                'end': today - timedelta(days=5),  # Bereits abgelaufen
                'kategorie': 'Gesundheit'
            }
        ]
        
        # Daten in die Datenbank einfügen
        for goal_data in goals_data:
            Goal.objects.create(**goal_data)
            
        self.stdout.write(self.style.SUCCESS(f'Erfolgreich {len(goals_data)} Beispielziele erstellt!'))