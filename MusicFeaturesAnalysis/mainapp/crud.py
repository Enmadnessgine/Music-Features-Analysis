from mainapp.services.reccobeatsapi.service import ReccoService, ReccoAPIError
from django.contrib.auth.models import User
from django.db import transaction
import os
from hashlib import sha256

from .models import AudioFile, Song, Features
from .utils import get_info, get_features

def file_hash(uploaded_file) -> str:
	hasher = sha256()
	for chunk in uploaded_file.chunks():
		hasher.update(chunk)
	return hasher.hexdigest()


@transaction.atomic
def create_song_f(user: User, file, title: str = "", artist: str = ""):
	hash = file_hash(file)
	service = ReccoService()
	audio, created = AudioFile.objects.get_or_create(
		file_hash=hash,
		defaults={
			"file": file,
			"size": file.size,
		}
	)
	
	file_path = audio.file.path

	if created:
		service = ReccoService()
		features = service.extract_from_audio(file_path)
		Features.objects.create(audio=audio, **features)

	song, created = Song.objects.get_or_create(
		user=user,
		audio=audio,
		defaults={
			"title": title,
			"artist": artist
		}
	)

	return song
	

@transaction.atomic
def save_top_tracks_with_features(user: User, top_tracks: list[dict]):
    for track in top_tracks:
        spotify_id = track["spotify_id"]

        reccobeats_id = get_info(spotify_id)
        if not reccobeats_id:
            print("No ReccoBeats match:", spotify_id)
            continue

        try:
            features_data = get_features(reccobeats_id)
            print("Features data:" , features_data)
        except Exception as e:
            print("Features error:", e)
            continue

        audio, _ = AudioFile.objects.get_or_create(
            file_hash=f"spotify:{spotify_id}",
            defaults={"file": None, "size": 0}
        )

        Song.objects.get_or_create(
            user=user,
            audio=audio,
            defaults={
                "track_id": spotify_id,
                "title": track["name"],
                "artist": track["artist"],
            }
        )
        
        if features_data is not None:
            Features.objects.update_or_create(
                audio=audio,
                defaults={
                    "acousticness": features_data.get("acousticness"),
                    "danceability": features_data.get("danceability"),
                    "energy": features_data.get("energy"),
                    "instrumentalness": features_data.get("instrumentalness"),
                    "liveness": features_data.get("liveness"),
                    "loudness": features_data.get("loudness"),
                    "speechiness": features_data.get("speechiness"),
                    "tempo": features_data.get("tempo"),
                    "valence": features_data.get("valence"),
                }
            )
        else:
            Features.objects.update_or_create(
                audio=audio,
                defaults={
                    "acousticness": 0,
                    "danceability": 0,
                    "energy": 0,
                    "instrumentalness": 0,
                    "liveness": 0,
                    "loudness": 0,
                    "speechiness": 0,
                    "tempo": 0,
                    "valence": 0,
                }
            )

        print(f"Saved: {track['name']}")


def get_user_songs(user: User):
	return Song.objects.filter(user=user).select_related('audio', 'audio__features')


def delete_user_song(user: User, song_id: int):
	try:
		song = Song.objects.get(id=song_id, user=user)
		song.delete()
		return True
	except Song.DoesNotExist:
		return False


			
