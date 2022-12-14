from django import forms
from .models import UserAccount
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password1', 'password2']

class SignInForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email').lower()
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            raise forms.ValidationError('User does not exist.')