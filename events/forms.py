from django import forms
from django.utils import timezone
from .models import Event

class EventAddForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'max_participants', 'image']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date', 
                'required': True,
                'class': '!w-full !rounded-lg !bg-transparent !shadow-sm !border-slate-200 dark:!border-slate-800 dark:!bg-white/5'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date', 
                'required': True,
                'class': '!w-full !rounded-lg !bg-transparent !shadow-sm !border-slate-200 dark:!border-slate-800 dark:!bg-white/5'
            }),
        }

    image = forms.ImageField(required=True)

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date <= timezone.now(): 
            raise forms.ValidationError("The start date must be greater than the current date.")
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date <= start_date:
            raise forms.ValidationError("End date must be greater than start date.")
        return end_date

    def clean_max_participants(self):
        max_participants = self.cleaned_data.get('max_participants')
        if max_participants <= 0:
            raise forms.ValidationError("The maximum number of participants must be a positive number.")
        return max_participants

class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'max_participants', 'image']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date', 
                'required': True,
                'class': '!w-full !rounded-lg !bg-transparent !shadow-sm !border-slate-200 dark:!border-slate-800 dark:!bg-white/5'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date', 
                'required': True,
                'class': '!w-full !rounded-lg !bg-transparent !shadow-sm !border-slate-200 dark:!border-slate-800 dark:!bg-white/5'
            }),
        }

    image = forms.ImageField(required=True)

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date <= timezone.now(): 
            raise forms.ValidationError("The start date must be greater than the current date.")
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date <= start_date:
            raise forms.ValidationError("End date must be greater than start date.")
        return end_date

    def clean_max_participants(self):
        max_participants = self.cleaned_data.get('max_participants')
        if max_participants <= 0:
            raise forms.ValidationError("The maximum number of participants must be a positive number.")
        return max_participants
