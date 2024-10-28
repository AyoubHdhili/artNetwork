from django.db import models

from django.conf import settings
from category.models import Category 


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=False)
    image = models.ImageField(upload_to='post_images/', blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', default=1)  # Replace 1 with your actual default category ID
                                 
    def __str__(self):
        return self.title

