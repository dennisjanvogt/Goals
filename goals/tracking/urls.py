from django.urls import path
from . import views

urlpatterns = [
    path('', views.goals_view, name='goals'),
    path('add/', views.add_goal, name='add_goal'),
    path('update/<int:goal_id>/', views.update_goal, name='update_goal'),
    path('delete/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path('update-progress/<int:goal_id>/', views.update_progress, name='update_progress'),
]