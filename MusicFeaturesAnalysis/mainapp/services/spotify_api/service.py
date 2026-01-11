import spotipy
from django.utils import timezone
from datetime import timedelta
from mainapp.models import SpotifyToken
from mainapp.spotify_auth import get_spotify_oauth
import requests

def get_spotify_client(user):
    token = SpotifyToken.objects.get(user=user)
    sp_oauth = get_spotify_oauth()

    if token.is_expired():
        new_token = sp_oauth.refresh_access_token(token.refresh_token)
        token.access_token = new_token["access_token"]
        token.expires_at = timezone.now() + timezone.timedelta(seconds=new_token["expires_in"])
        token.save()

    return spotipy.Spotify(auth=token.access_token)


def get_spotify_client(user):
    token = SpotifyToken.objects.get(user=user)
    sp_oauth = get_spotify_oauth()

    if token.expires_at <= timezone.now():
        token_info = sp_oauth.refresh_access_token(token.refresh_token)

        token.access_token = token_info["access_token"]
        token.expires_at = timezone.now() + timedelta(
            seconds=token_info["expires_in"]
        )
        token.save()

    return spotipy.Spotify(auth=token.access_token)


def get_user_top_tracks(user, limit=20, time_range="medium_term"):
    """
    time_range:
    - short_term (4 weeks)
    - medium_term (6 months)
    - long_term (years)
    """

    sp = get_spotify_client(user)

    results = sp.current_user_top_tracks(
        limit=limit,
        time_range=time_range
    )

    return [
        {
            "spotify_id": track["id"],
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "image": track["album"]["images"][0]["url"]
            if track["album"]["images"] else None,
            "preview_url": track["preview_url"],
        }
        for track in results["items"]
    ]
