from django.db import models

# Create your models here.
# notes/models.py
from django.db import models
from django.contrib.auth.models import User
import markdown
from django.utils.safestring import mark_safe


class Topic(models.Model):
    """Model for organizing notes into topics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Note(models.Model):
    """Model for storing individual notes with markdown content"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-is_pinned', '-updated_at']
    
    def get_formatted_content(self):
        """Returns the note content formatted as HTML using markdown"""
        html = markdown.markdown(
            self.content,
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables',
                'markdown.extensions.nl2br',
                'markdown.extensions.extra'
            ]
        )
        return mark_safe(html)