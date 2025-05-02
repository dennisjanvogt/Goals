from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.goals_view, name='goals'),
]