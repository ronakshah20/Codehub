from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Repository(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Automatically updates on save

    def __str__(self):
        return f'{self.owner.username}/{self.name}'
    class Meta:
        unique_together = ('owner', 'name')

class RepoFile(models.Model):
    """
    Represents a single file within a repository.
    """
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='files')
    file_path = models.CharField(max_length=512)
    content = models.TextField(blank=True) # The code or text of the file
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.repository.name}/{self.file_path}'
    
    class Meta:
        # Prevent duplicate file paths within the same repository
        unique_together = ('repository', 'file_path')
