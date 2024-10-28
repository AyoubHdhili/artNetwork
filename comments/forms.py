from django import forms
from django.core.exceptions import ValidationError
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        
        # Check if content is empty
        if not content:
            raise ValidationError("Content cannot be empty.")
        
        # Check for minimum and maximum length
        min_length = 5  # Set your minimum length
        max_length = 500  # Set your maximum length
        
        if len(content) < min_length:
            raise ValidationError(f"Content must be at least {min_length} characters long.")
        
        if len(content) > max_length:
            raise ValidationError(f"Content must not exceed {max_length} characters.")
        
        # Example: Check for forbidden words (optional)
        forbidden_words = ["spam", "offensive"]
        if any(word in content.lower() for word in forbidden_words):
            raise ValidationError("Content contains forbidden words.")
        
        return content
