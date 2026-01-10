from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .spotify_auth import get_spotify_oauth
from .services.spotify_api.service import get_spotify_client, get_user_top_tracks
from .forms import UserRegisterForm, UserLoginForm
from .models import Song, SpotifyToken



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
    tracks = get_user_top_tracks(request.user, limit=50)
    print(tracks)
    return render(request, "mainapp/profile.html", {"user": request.user, "user_songs": user_songs, "tracks": tracks})


#SPOTIFY_API
def spotify_login(request):
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@csrf_exempt
@login_required
def spotify_callback(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponseBadRequest("No code")

    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.get_access_token(code)

    SpotifyToken.objects.update_or_create(
        user=request.user,
        defaults={
            "access_token": token_info["access_token"],
            "refresh_token": token_info.get("refresh_token", ""),
            "expires_at": timezone.now() + timedelta(seconds=token_info["expires_in"]),
        }
    )

    return redirect("profile")

"""""
@login_required
def top_tracks(request):
    tracks = get_user_top_tracks(request.user, limit=50)
    print(tracks)
    return render(request, "mainapp/profile.html", {"tracks": tracks})
"""""
