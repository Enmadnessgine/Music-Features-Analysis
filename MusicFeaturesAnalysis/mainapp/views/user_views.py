import token
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import UserRegisterForm, UserLoginForm

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = UserLoginForm()
    return render(request, "mainapp/login.html", {"form": form})

def signin(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SignIn is success!")
            return redirect("login")
        else:
            messages.error(request, "SignIn is failed!")
    else:
        form = UserRegisterForm()
    return render(request, "mainapp/signin.html", {"form": form})

@login_required
def user_logout(request):
    logout(request)
    return redirect("index")