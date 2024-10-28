from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Reclamation(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('solved', 'Solved'),
        ('not_accepted', 'Not Accepted'),
    ], default='pending')

    def __str__(self):
        return self.title


class Response(models.Model):
    reclamation = models.ForeignKey(Reclamation, related_name='responses', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.reclamation.title} by Support Technician"
