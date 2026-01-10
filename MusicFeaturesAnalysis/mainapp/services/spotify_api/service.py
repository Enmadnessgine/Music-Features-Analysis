import spotipy
from django.utils import timezone
from mainapp.models import SpotifyToken
from mainapp.spotify_auth import get_spotify_oauth

def get_spotify_client(user):
    token = SpotifyToken.objects.get(user=user)
    sp_oauth = get_spotify_oauth()

    if token.is_expired():
        new_token = sp_oauth.refresh_access_token(token.refresh_token)
        token.access_token = new_token["access_token"]
        token.expires_at = timezone.now() + timezone.timedelta(seconds=new_token["expires_in"])
        token.save()

    return spotipy.Spotify(auth=token.access_token)
