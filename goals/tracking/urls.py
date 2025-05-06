from django.urls import path
from . import views

urlpatterns = [
    path('', views.goals_view, name='goals'),
    path('add/', views.add_goal, name='add_goal'),
    path('update/<int:goal_id>/', views.update_goal, name='update_goal'),
    path('delete/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path('update-progress/<int:goal_id>/', views.update_progress, name='update_progress'),
    path('yearly-goals/', views.yearly_goals, name='yearly_goals'),
    path('yearly-goals/add/', views.add_yearly_goal, name='add_yearly_goal'),
    path('yearly-goals/update/<int:goal_id>/', views.update_yearly_goal, name='update_yearly_goal'),
    path('yearly-goals/delete/<int:goal_id>/', views.delete_yearly_goal, name='delete_yearly_goal'),
    path('yearly-goals/quick-update/<int:goal_id>/', views.quick_update_yearly_goal, name='quick_update_yearly_goal'),
]