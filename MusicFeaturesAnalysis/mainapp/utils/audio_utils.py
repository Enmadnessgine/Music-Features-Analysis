from hashlib import sha256
from django.contrib.auth.models import User
from django.db import transaction
from mainapp.services.reccobeatsapi.service import ReccoService
from ..models import AudioFile, Song, Features
from mainapp.services.model_db import ModelData
from .search_utils import build_features_dict

audio_repo = ModelData(AudioFile)
song_repo = ModelData(Song)
features_repo = ModelData(Features)


def file_hash(uploaded_file) -> str:
    hasher = sha256()
    for chunk in uploaded_file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()


@transaction.atomic
def create_song_f(user: User, file, title: str = "", artist: str = ""):
    file_hash_value = file_hash(file)

    audio, created = audio_repo.get_or_create(
        kwargs={"file_hash": file_hash_value},
        defaults={
            "file": file,
            "size": file.size,
        },
    )

    if created:
        service = ReccoService()
        features_data = service.extract_from_audio(audio.file.path)

        features_repo.get_or_update(
            kwargs={"audio": audio}, defaults=build_features_dict(features_data)
        )

    song, _ = song_repo.get_or_create(
        kwargs={
            "user": user,
            "audio": audio,
        },
        defaults={
            "title": title,
            "artist": artist,
        },
    )

    return song