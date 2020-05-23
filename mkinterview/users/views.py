from django.shortcuts import render
from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model 


Account = get_user_model()

def home(request):
    return render(request,'users/home.html')

def userhome(request):
    return render(request,'users/userhome.html')

def register(request):
    context = {}
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email,password=raw_password)
            login(request,user)
            messages.success(request,f'Your account has been created!! Now you are able to login!')
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = UserRegisterForm()
        context['registration_form'] = form
    return render(request,'users/register.html',context)
