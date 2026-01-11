import requests
from .services.spotify_api.service import get_user_top_tracks
from functools import wraps

def des(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as e:
			print(f"API call failed: {e}")
			return {"error": "id is not valid"}
	return wrapper

def get_info(spotify_id: str) -> str | None:
	r = requests.get(f"https://api.reccobeats.com/v1/track?ids={spotify_id}")
	r.raise_for_status()

	data = r.json()
	if not data.get("content"):
		return None

	return data["content"][0]["id"]

@des
def get_features(id):
	res = requests.get(f"https://api.reccobeats.com/v1/track/{id}/audio-features")
	if res.status_code == 200:
		json_obj = res.json()
		print(json_obj)
		return json_obj
	else:
		raise ConnectionError("Try later")

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

		result.append({
			**track,
			"reccobeats_id": reccobeats_id,
			"audio_features": features
		})

	return result

def info_from_s_to_r(spotify_id: str):
	rid = get_info(spotify_id)
	data = get_features(rid)
	return data