# notes/forms.py
from django import forms
from .models import Topic, Note

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thema Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Beschreibung (optional)'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'topic', 'content', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titel der Notiz'}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 15, 
                'placeholder': '# Markdown-Formatierung unterstützt\n\n**Fett**, *kursiv*, [Link](http://example.com), \n```\nCode-Block\n```',
                'style': 'font-family: monospace;'
            }),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['topic'].queryset = Topic.objects.filter(user=user)