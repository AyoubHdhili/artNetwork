# reclamation/forms.py
from django import forms
from .models import Reclamation

class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['title', 'description']
