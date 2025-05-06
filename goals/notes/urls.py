# notes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_home, name='notes_home'),
    path('note/<int:note_id>/', views.view_note, name='view_note'),
    path('note/add/', views.add_note, name='add_note'),
    path('note/edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('note/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('topic/add/', views.add_topic, name='add_topic'),
    path('topic/edit/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('topic/delete/<int:topic_id>/', views.delete_topic, name='delete_topic'),
]