from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from .models import Song


def index(request):
    return render(request, "base.html")


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'mainapp/login.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'SignIn is success!')
            return redirect('login')
        else:
            messages.error(request, 'SignIn is failed!')
    else:
        form = UserRegisterForm()
    return render(request, 'mainapp/signin.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('')

def profile(request):
    user_songs = Song.objects.filter(user=request.user).select_related("audio", "audio__features")
    return render(request, "mainapp/profile.html", {"user": request.user, "user_songs": user_songs})