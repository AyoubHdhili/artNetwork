from django.db import models
from users.models import User

class ChatGroup (models.Model):
    group_name = models.CharField(max_length=128, unique=True, default='General')
    admin = models.ForeignKey(User, related_name="groupchats", blank=True, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    def __str__(self):
        return self.group_name
    
class GroupMessage (models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models. CASCADE)
    author = models.ForeignKey(User, on_delete=models. CASCADE)
    body = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self) :
        return f'{self.author.username} r: {self.body}'
    
    class Meta:
        ordering = ['-created_at']