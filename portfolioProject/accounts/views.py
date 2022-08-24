from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterUserForm

# Create your views here.
def login_user(request):
    if request.user.is_authenticated:
        messages.success(request, ("Already logged in"))
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request, ("There was an error logging in, try again..."))
                return redirect('login')
        else:
            return render(request, "accounts/login.html", {})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ("Succesfully logged out"))
    return redirect('login')

def register_user(request):
    if request.user.is_authenticated:
        messages.success(request, ("Already logged in"))
        return redirect('home')
    else:
        if request.method == "POST":
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username = username, password = password)
                login(request, user)
                messages.success(request, 'Succesfully signed up')
                return redirect('home')
        else:
            form = RegisterUserForm()
    return render(request, "accounts/register.html", {
        'form':form,
    })

@login_required
def view_profile(request):
    return render(request, "accounts/viewProfile.html", {})