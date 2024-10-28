from django.contrib import admin
from .models import Post
from category.models import Category  # Import Category if needed

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'category')  # Include category in display
    search_fields = ('title', 'content')
    list_filter = ('category',)  # Filter by category in the admin

admin.site.register(Post, PostAdmin)
