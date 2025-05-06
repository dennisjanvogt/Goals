# notes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from .models import Topic, Note
from .forms import TopicForm, NoteForm

@login_required
def notes_home(request):
    """Display list of notes or filtered by topic"""
    topic_id = request.GET.get('topic')
    search_query = request.GET.get('q')
    
    # Get all topics for sidebar
    topics = Topic.objects.filter(user=request.user)
    
    # Filter notes based on topic or search query
    if topic_id:
        notes = Note.objects.filter(user=request.user, topic_id=topic_id)
        current_topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    elif search_query:
        notes = Note.objects.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query),
            user=request.user
        )
        current_topic = None
    else:
        notes = Note.objects.filter(user=request.user)
        current_topic = None
    
    context = {
        'topics': topics,
        'notes': notes,
        'current_topic': current_topic,
        'search_query': search_query,
    }
    return render(request, 'notes/home.html', context)

@login_required
def view_note(request, note_id):
    """Display a single note with formatted content"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    topics = Topic.objects.filter(user=request.user)
    
    context = {
        'note': note,
        'topics': topics,
    }
    return render(request, 'notes/view_note.html', context)

@login_required
def add_note(request):
    """Add a new note"""
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Notiz erfolgreich erstellt!')
            return redirect('view_note', note_id=note.id)
    else:
        # Pre-select topic if provided in URL
        initial_data = {}
        topic_id = request.GET.get('topic')
        if topic_id:
            initial_data['topic'] = topic_id
        
        form = NoteForm(user=request.user, initial=initial_data)
    
    topics = Topic.objects.filter(user=request.user)
    context = {
        'form': form,
        'topics': topics,
        'is_add_mode': True,
    }
    return render(request, 'notes/add_edit_note.html', context)

@login_required
def edit_note(request, note_id):
    """Edit an existing note"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notiz erfolgreich aktualisiert!')
            return redirect('view_note', note_id=note.id)
    else:
        form = NoteForm(instance=note, user=request.user)
    
    topics = Topic.objects.filter(user=request.user)
    context = {
        'form': form,
        'note': note,
        'topics': topics,
        'is_add_mode': False,
    }
    return render(request, 'notes/add_edit_note.html', context)

@login_required
def delete_note(request, note_id):
    """Delete a note"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    if request.method == 'POST':
        topic_id = note.topic.id
        note.delete()
        messages.success(request, 'Notiz erfolgreich gelöscht!')
        base_url = reverse('notes_home')
        return redirect(f'{base_url}?topic={topic_id}')
    
    topics = Topic.objects.filter(user=request.user)
    context = {
        'note': note,
        'topics': topics,
    }
    return render(request, 'notes/delete_note.html', context)

@login_required
def add_topic(request):
    """Add a new topic"""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            messages.success(request, 'Thema erfolgreich erstellt!')
            base_url = reverse('notes_home')
            return redirect(f'{base_url}?topic={topic.id}')
    else:
        form = TopicForm()
    
    topics = Topic.objects.filter(user=request.user)
    context = {
        'form': form,
        'topics': topics,
        'is_add_mode': True,
    }
    return render(request, 'notes/add_edit_topic.html', context)

@login_required
def edit_topic(request, topic_id):
    """Edit an existing topic"""
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thema erfolgreich aktualisiert!')
            base_url = reverse('notes_home')
            return redirect(f'{base_url}?topic={topic.id}')
    else:
        form = TopicForm(instance=topic)
    
    topics = Topic.objects.filter(user=request.user)
    context = {
        'form': form,
        'topic': topic,
        'topics': topics,
        'is_add_mode': False,
    }
    return render(request, 'notes/add_edit_topic.html', context)

@login_required
def delete_topic(request, topic_id):
    """Delete a topic and all associated notes"""
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    
    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Thema und alle zugehörigen Notizen erfolgreich gelöscht!')
        return redirect('notes_home')
    
    topics = Topic.objects.filter(user=request.user)
    context = {
        'topic': topic,
        'topics': topics,
        'note_count': topic.notes.count(),
    }
    return render(request, 'notes/delete_topic.html', context)