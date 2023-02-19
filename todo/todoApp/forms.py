from django import forms
from .models import Note

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=150)
    password = forms.CharField(label='password', max_length=128, widget=forms.PasswordInput) 

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=150)
    typeEmailX = forms.EmailField(label='typeEmailX', max_length=254)
    typePasswordX = forms.CharField(label='typePasswordX', max_length=128, widget=forms.PasswordInput)


class ToDoForm(forms.Form):
    title = forms.CharField(max_length=100, label='title')
    content = forms.CharField(max_length=1000, label='content')
    due_date = forms.DateTimeField(label='due_date')