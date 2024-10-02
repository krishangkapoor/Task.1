from django import forms
from .models import Todo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['task_name', 'is_done']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user