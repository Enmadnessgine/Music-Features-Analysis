import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
from .spotify_cache import NullCacheHandler

def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=settings.SPOTIFY_SCOPES,
        cache_handler=NullCacheHandler(),
        show_dialog=True     # FOR DEBUGGING
        )