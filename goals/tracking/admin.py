# Update tracking/admin.py
from django.contrib import admin
from .models import Goal, YearlyGoal

# Register your models here.
admin.site.register(Goal)
admin.site.register(YearlyGoal)