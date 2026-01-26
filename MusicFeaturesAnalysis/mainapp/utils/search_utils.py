import requests
from .info_utils import info_from_s_to_r, get_features, build_features_dict

def resolve_song(q: str):
	sp_id = None
	rb_id = None

	if len(q) == 22:
		sp_id = q
		data = info_from_s_to_r(sp_id)
		rb_id = data.get("id", None)
	else:
		sp_id = ""
		rb_id = q
		data = get_features(q)
		
	return sp_id, rb_id, data

def build_info(sp_id, rb_id, data, user=None):
	info = {
		"spotify_id": sp_id,
		"reccobeats_id": rb_id,
		"link": data.get('href'),
	}
	
	data = build_features_dict(data)

	if user:
		info["user"] = user

	return info