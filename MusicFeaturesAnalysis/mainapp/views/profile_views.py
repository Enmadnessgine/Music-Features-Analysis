from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from ..forms import AudioUploadForm
from ..models import Song, SpotifyToken
from ..utils.spotify_utils import save_top_tracks_with_features
from django.core.paginator import Paginator
from mainapp.services.spotify_api.service import get_user_top_tracks
from mainapp.services.spotify_api.utils import cache_tokens, get_access_token, get_refresh_token
from DataModifying.models.Classifier import GenreClassifier
from ..services.model_db import ModelData
from ..models import AudioFile, Features, Song
from ..utils.info_utils import build_features_dict_
from services.models_crud.crud import audio_repo, song_repo, features_repo



genremodel = GenreClassifier(model_path="DataModifying/models/artifacts/genre_classifier.pkl")
audio_model = ModelData(AudioFile)
features_model = ModelData(Features)
song_model = ModelData(Song)
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
	analizer_data_ = request.session.pop("analizer_data_", None)
	
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
			"analizer_data_": analizer_data_,
		},
	)

@login_required
def load_ts(request):
	refresh_token = get_refresh_token(request.user.id)
	
	if not refresh_token:
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
	
def load_analizer_info(request):
	analizer_data = {}
	tracks = song_repo.get_all(request.user)
	
	for track in tracks:
		genre = track.genre
		if len(genre) > 0:
			analizer_data[genre] += 1
	
	max_data = max(analizer_data, key=lambda k: analizer_data[k])
	analizer_data_ = max_data if max_data is not None else "we haven't data from service"
	
	return JsonResponse({"status": 200, "data": analizer_data_})