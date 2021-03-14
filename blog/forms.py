from django import forms
from blog.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=['body']

class DummyForm(forms.ModelForm):
    class Meta:
        model=Dummy
        fields=['title','content','first_img','second_img','third_img','status']
        labels={'first_img':'Image1','second_img':'Image2','third_img':'Image3'}

class EditDummyForm(forms.ModelForm):
    class Meta:
        model=Dummy
        fields=['title','content','first_img','second_img','third_img','status']
        labels={'first_img':'Image1','second_img':'Image2','third_img':'Image3'}

class UserForm(UserCreationForm):
    first_name=forms.CharField(max_length=100, required=True)
    last_name=forms.CharField(max_length=100, required=True)
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=['first_name','last_name', 'email','username','password1','password2']