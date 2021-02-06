from django import forms
from blog.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','slug','content','status']

class DummyForm(forms.ModelForm):
    class Meta:
        model=Dummy
        fields=['title','content','status']

class UserForm(UserCreationForm):
    first_name=forms.CharField(max_length=100, required=True)
    last_name=forms.CharField(max_length=100, required=True)
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=['first_name','last_name', 'email','username','password1','password2']