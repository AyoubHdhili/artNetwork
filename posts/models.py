from django.db import models
from django.contrib.auth import get_user_model

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title