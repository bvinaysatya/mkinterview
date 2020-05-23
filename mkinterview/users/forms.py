from django import forms
from account.models import Account, Profile
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email               = forms.EmailField(max_length=60, help_text='Required! Enter email address')
    fname               = forms.CharField(max_length=50, help_text='Required! Enter first name')
    fullname            = forms.CharField(max_length=50, help_text='Required! Enter full name')    
    mobile              = forms.IntegerField() 
    
    model = Account
    fields = ['fname','fullname','mobile','email','password1','password2']


