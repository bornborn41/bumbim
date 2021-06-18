from django import forms
from .models import Author, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from djrichtextfield.widgets import RichTextWidget


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.CharField(widget=RichTextWidget())
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['username', 'email', 'image']

        widgets = {

            'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea', 'style': 'font-weight: bold; font-size: 150%;', 'rows': '3', 'cols': '30'})
        }


class LoginForm(UserCreationForm):
    class Meta:
        model = Author
        fields = ['username', 'password']
        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-controls', 'type': 'password', 'name': 'password'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Author
        fields = ['username', 'email', 'password1', 'password2', 'image']
