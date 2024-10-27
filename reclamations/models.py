# reclamation/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class Reclamation(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
