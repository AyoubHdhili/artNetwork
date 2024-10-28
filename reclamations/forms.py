# reclamation/forms.py
from django import forms
from .models import Reclamation, Response

class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['title', 'description']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']