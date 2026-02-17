from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from requests import request
from ..forms import AudioUploadForm
from ..models import Song, SpotifyToken
from ..utils.spotify_utils import save_top_tracks_with_features
from django.core.paginator import Paginator
from mainapp.services.spotify_api.service import get_user_top_tracks
from mainapp.services.spotify_api.utils import get_refresh_token
from DataModifying.models.Classifier import GenreClassifier
from DataModifying.models.registry import ModelRegistry
from ..models import AudioFile, Features, Song
from ..utils.info_utils import build_stats
from mainapp.services.models_crud.crud import audio_repo, song_repo, features_repo, statistics_repo

genremodel = GenreClassifier(model_path="DataModifying/models/artifacts/genre_classifier_v02.pkl")
user_stats = ModelRegistry.get("user_profile")

@login_required
def profile(request):
	user_songs = Song.objects.filter(user=request.user).select_related(
		"audio", "audio__features"
	)

	form = AudioUploadForm()
	spotify_connected = SpotifyToken.objects.filter(user=request.user).exists()
	analizer_data_ = request.session.pop("analizer_data_", None)
	
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


@login_required
def load_stats(request):
	all_genres_percent = {}
	features_values_average = {}
	most_common = {}

	existing_stats_qs = statistics_repo.get_statistic(request.user)

	if existing_stats_qs.exists():
		statistic = existing_stats_qs.first()
		most_common = statistic.most_common_genre_percent or {}
		all_genres_percent = statistic.all_genres_percent or {}
		features_values_average = statistic.features_values_average or {}

	else:
		stats = user_stats.predict(user=request.user)

		total_songs = int(stats.get("count", 0))
		rarest_genre = stats.get("rarest_subgenre") or "N/A"
		top_genre = stats.get("top_subgenre") or "N/A"
		top_genre_percent = float(stats.get("top_subgenre_percent") or 0)

		all_genres_percent = stats.get("all_subgenre_percent") or {}
		features_values_average = stats.get("mean_features") or {}

		diversity_score = float(stats.get("diversity_score", 0) or 0)
		mood_score = float(stats.get("mood", 0) or 0)

		most_common = {top_genre: top_genre_percent} if top_genre else {}

		statistic, created = statistics_repo.create_or_update(
			user=request.user,
			total_songs=total_songs,
			tog_genre=most_common,
			rarest_genre=rarest_genre,
			all_genres_percent=all_genres_percent,
			features_values_average=features_values_average,
			diversity_score=diversity_score,
			mood_score=mood_score,
		)

	data = build_stats(
		statistic,
		most_common,
		all_genres_percent,
		features_values_average
	)

	return render(request, "mainapp/stats.html", context=data)


def load_analizer_info(request):
	analizer_data = {}
	tracks = song_repo.get_all(request.user)

	for track in tracks:
		genre = track.genre
		if genre:
			analizer_data[genre] = analizer_data.get(genre, 0) + 1

	if not analizer_data:
		return JsonResponse({
			"status": 200,
			"data": "We haven't data from service!"
		})

	max_data = max(analizer_data, key=analizer_data.get)

	answer = f"You mostly listen: {max_data}"
	return JsonResponse({
		"status": 200,
		"data": answer,
	})