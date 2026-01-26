from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import AudioUploadForm
from ..models import Song, SpotifyToken
from ..utils.spotify_utils import save_top_tracks_with_features
from django.core.paginator import Paginator
from mainapp.services.spotify_api.service import get_user_top_tracks
from mainapp.services.spotify_api.utils import cache_tokens, get_access_token, get_refresh_token


@login_required
def profile(request):
    user_songs = Song.objects.filter(user=request.user).select_related(
        "audio", "audio__features"
    )
    form = AudioUploadForm()
    spotify_connected = SpotifyToken.objects.filter(user=request.user).exists()
    spotify_con = SpotifyToken.objects.filter(user=request.user).first()
    
    if spotify_connected:
        print("DB access_token:", spotify_con.access_token)
        print("DB refresh_token:", spotify_con.refresh_token)
    
    access_token = get_access_token(request.user.id)
    refresh_token = get_refresh_token(request.user.id)
    
    if access_token:
        print("Cached access_token:", access_token)
    elif refresh_token:
        print("Access token відсутній, є refresh_token:", refresh_token)
    
    return render(
        request,
        "mainapp/profile.html",
        {
            "user": request.user,
            "user_songs": user_songs,
            "form": form,
            "spotify_connected": spotify_connected,
        },
    )

@login_required
def load_ts(request):
    if not SpotifyToken.objects.filter(user=request.user).exists():
        messages.warning(request, "Please connect your Spotify account first.")
        return redirect("profile")

    tracks = get_user_top_tracks(request.user, limit=20)
    save_top_tracks_with_features(request.user, tracks)

    paginator = Paginator(tracks, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "mainapp/top_songs.html",
        {"user": request.user, "tracks": tracks, "page_obj": page_obj},
    )