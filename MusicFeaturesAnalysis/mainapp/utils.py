import requests
from services.spotify_api.service import get_user_top_tracks

def get_info(id):
	params = {"ids": f"GET /track?ids={id}"}
	r = requests.get(f"https://api.reccobeats.com/v1/track?ids={id}")
	try:
		data = r.json()
		if data['content']:
			return data
		else:
			return data
	except Exception as e:
		raise e
	
def get_features(id):
	res = requests.get(f"https://api.reccobeats.com/v1/track/{id}/audio-features")
	if res.status_code == 200:
		json_obj = res.json()
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

