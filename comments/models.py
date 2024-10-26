from django.db import models
from django.contrib.auth import get_user_model

class Comment(models.Model):
    content = models.TextField()  
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments') 

    def __str__(self):
        # Check if the user has a 'fullname' attribute instead of 'username'
        fullname = getattr(self.author, 'fullname', 'Unknown Author')
        return f'{fullname}: {self.content[:20]}...'
