from django import forms
from django.contrib.auth import get_user_model
import re 
User = get_user_model()



class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': '!w-full !rounded-lg !bg-transparent !shadow-sm !border-slate-200 dark:!border-slate-800 dark:!bg-white/5',
        }),
        min_length=8,  
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': '!w-full !rounded-lg !bg-transparent !shadow-sm !border-slate-200 dark:!border-slate-800 dark:!bg-white/5',
        }),
        label='Confirmer le mot de passe',
        min_length=8,  
    )
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',  
            'class': '!w-full !rounded-lg !bg-transparent !shadow-sm !border-slate-200 dark:!border-slate-800 dark:!bg-white/5',
        }),
        required=False 
    )

    class Meta:
        model = User
        fields = ['email', 'fullname', 'phone', 'birthday', 'address', 'password']  

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and (len(phone) != 8 or not re.match(r'^\d{8}$', phone)):
            raise forms.ValidationError("The phone number must contain exactly 8 digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and len(password) < 8:
            self.add_error('password', "The password must contain at least 8 characters.")
        
        if password_confirm and len(password_confirm) < 8:
            self.add_error('password_confirm', "The password confirmation must contain at least 8 characters.")
        
        if password != password_confirm:
             self.add_error('password_confirm', "Passwords do not match.")

        return cleaned_data




class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs={
            'class': '!w-full !rounded-lg !bg-transparent !shadow-sm !border-slate-200 dark:!border-slate-800 dark:!bg-white/5',
        }),
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={
            'class': '!w-full !rounded-lg !bg-transparent !shadow-sm !border-slate-200 dark:!border-slate-800 dark:!bg-white/5',
        }),
    )

class UserUpdateForm(forms.ModelForm):
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',  
            'class': '!w-full !rounded-lg !bg-transparent !shadow-sm !border-slate-200 dark:!border-slate-800 dark:!bg-white/5',
        }),
        required=False 
    )

    class Meta:
        model = User
        fields = ['fullname', 'phone', 'birthday', 'address', 'user_photo']  

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['user_photo'].required = False
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and (len(phone) != 8 or not re.match(r'^\d{8}$', phone)):
            raise forms.ValidationError("The phone number must contain exactly 8 digits.")
        return phone
