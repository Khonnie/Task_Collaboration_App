from django import forms
from .models import Task, UserProfile

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task

        # Only show these fields to the user
        fields = ['title']

        # Bootstrap styling within the form
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task...'
            }),
            # 'completed': forms.CheckboxInput(attrs={
            #     'class': 'form-check-input'
            # })
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture']
