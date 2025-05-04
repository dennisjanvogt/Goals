from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.add_todo, name='add_todo'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('toggle/<int:todo_id>/', views.toggle_complete, name='toggle_complete'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('update-priority/<int:todo_id>/', views.update_priority, name='update_priority'),
]