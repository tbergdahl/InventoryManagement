from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.hashers import make_password

class CreateUserForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.UType.choices)
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'user_type']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user