from .models import AudioFile, Song, Features
from mainapp.services.reccobeatsapi.service import ReccoService, ReccoAPIError
from django.contrib.auth.models import User
from django.db import transaction
import os
from hashlib import sha256


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
	

def get_user_songs(user: User):
	return Song.objects.filter(user=user).select_related('audio', 'audio__features')


def delete_user_song(user: User, song_id: int):
	try:
		song = Song.objects.get(id=song_id, user=user)
		song.delete()
		return True
	except Song.DoesNotExist:
		return False