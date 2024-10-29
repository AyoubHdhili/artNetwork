from django.forms import ModelForm
from django import forms
from .models import *

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Write your message',
                'class': 'w-full resize-none bg-secondery rounded-full px-4 p-2',
                'maxlength': '300',
                'autofocus': True
            }),
        }
        
class ChatGroupEditForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # Change this to filter users as needed
        widget=forms.CheckboxSelectMultiple,  # Change to other widgets if needed
        required=False  # Make it optional if needed
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,  # Number of lines visible
            'cols': 40,  # Width of the textarea
            'maxlength': 300  # Set HTML attribute for max length
        }),
        label="Description"
    )
    class Meta:
        model = ChatGroup
        fields = ['group_name', 'description', 'is_private', 'members'] 
        
class ChatGroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'flex flex-col gap-2'}),  # Adjust styles as needed
        required=False  # Set to True if you want it to be required
    )
    class Meta:
        model = ChatGroup
        fields = ['group_name', 'admin', 'members', 'description', 'is_private']
        widgets = {
            'group_name': forms.TextInput(attrs={'placeholder': 'Group Name', 'class': 'lg:w-1/2 w-full'}),
            'admin': forms.Select(attrs={'class': '!border-0 !rounded-md lg:w-1/2 w-full'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter your group description', 'class': 'w-full', 'rows': 5}),
        }
        
    def clean_group_name(self):
        group_name = self.cleaned_data.get('group_name')
        if ChatGroup.objects.filter(group_name=group_name).exists():
            raise forms.ValidationError('This group name is already taken.')
        return group_name
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            if len(description) < 10 or len(description) > 255:
                raise forms.ValidationError('Description must be between 10 and 255 characters long.')
        return description
    
    def clean_members(self):
        members = self.cleaned_data.get('members')
        if not members:
            raise forms.ValidationError('At least one member must be selected.')
        return members

    def clean_admin(self):
        admin = self.cleaned_data.get('admin')
        if not admin:
            raise forms.ValidationError('You must choose an admin to this group.')
        return admin

    def clean_group_name(self):
        group_name = self.cleaned_data.get('group_name')
        if group_name and group_name[0].isdigit():
            raise forms.ValidationError('Group name cannot start with a number.')
        return group_name

    def clean(self):
        cleaned_data = super().clean()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['admin'].empty_label = "Select Admin"