from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from ..spotify_auth import get_spotify_oauth
from ..models import SpotifyToken
from mainapp.services.spotify_api.utils import cache_tokens
from mainapp.services.models_crud.crud import spotify_repo

@login_required
def spotify_login(request):
    sp_oauth = get_spotify_oauth()
    return redirect(sp_oauth.get_authorize_url())

@csrf_exempt
@login_required
def spotify_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect("profile")

    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.get_access_token(code)
    expires_at = timezone.now() + timedelta(seconds=token_info["expires_in"])

    spotify_repo.create_or_update(request.user, token_info["access_token"], token_info.get("refresh_token"), expires_at)
    cache_tokens(
        access_token=token_info["access_token"],
        refresh_token=token_info.get("refresh_token"),
        user_id=request.user.id,
    )
    
    return redirect("profile")