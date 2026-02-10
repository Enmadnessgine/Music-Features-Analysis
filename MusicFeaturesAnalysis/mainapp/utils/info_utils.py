import requests
from ..services.spotify_api.service import get_user_top_tracks
from ..models import Features
from mainapp.services.reccobeatsapi.service import ReccoAPIError


def get_info(spotify_id: str) -> str | None:
	r = requests.get(f"https://api.reccobeats.com/v1/track?ids={spotify_id}")
	r.raise_for_status()

	data = r.json()
	if not data.get("content"):
		return None

	return data["content"][0]["id"]

def get_features(id):
	try:
		res = requests.get(
			f"https://api.reccobeats.com/v1/track/{id}/audio-features", timeout=10
		)
	except requests.RequestException as e:
		raise ReccoAPIError("ReccoBeats unavailable") from e

	if res.status_code == 404:
		return None

	res.raise_for_status()

	return res.json()

def top_songs_info(user, limit=20, time_range="medium_term"):
	top_tracks = get_user_top_tracks(user, limit, time_range)
	result = []

	for track in top_tracks:
		spotify_id = track["spotify_id"]

		info = get_info(spotify_id)

		if not info.get("content"):
			continue

		reccobeats_id = info["content"][0]["id"]
		features = get_features(reccobeats_id)

		result.append(
			{**track, "reccobeats_id": reccobeats_id, "audio_features": features}
		)

	return result


def info_from_s_to_r(spotify_id: str):
	rid = get_info(spotify_id)
	data = get_features(rid)
	return data

FEATURE_FIELDS = (
	"acousticness",
	"danceability",
	"energy",
	"instrumentalness",
	"liveness",
	"loudness",
	"speechiness",
	"tempo",
	"valence",
)

def build_features_dict(data: dict | None):
	if not data:
		return {key: 0 for key in FEATURE_FIELDS}

	return {key: data.get(key) for key in FEATURE_FIELDS}

def build_features_dict_(features: Features | None):
	if not features:
		return {key: 0 for key in FEATURE_FIELDS}

	return {key: getattr(features, key) for key in FEATURE_FIELDS}

def build_stats(statistic, most_common: dict):
	top_genre = list(most_common.keys())[0] if most_common else "N/A"
	top_genre_percent = list(most_common.values())[0] if most_common else 0

	data = {
		"status": 200,
		"data": {
			"Total Songs": getattr(statistic, "total_songs", 0),
			"Top Genre": top_genre,
			"Top Genre %": top_genre_percent,
			"Rarest Genre": getattr(statistic, "rarest_genre", "N/A"),
			"Diversity Score": getattr(statistic, "diversity_score", 0),
			"Mood Score": getattr(statistic, "mood_score", 0),
		}
	}
	
	return data