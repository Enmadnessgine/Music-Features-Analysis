from django.contrib.auth.models import User
from django.db import transaction
from mainapp.services.reccobeatsapi.service import ReccoService
from .search_utils import build_features_dict
from .utils import file_hash
from mainapp.services.models_crud.crud import audio_repo, song_repo, features_repo
from DataModifying.models.Classifier import GenreClassifier

classifier = GenreClassifier(model_path="DataModifying/models/artifacts/genre_classifier_v02.pkl")

@transaction.atomic
def create_song_f(user: User, file, title: str = "", artist: str = ""):
    audio, created = audio_repo.create_audio(file_hash(file), file)
    if created:
        service = ReccoService()
        features_data = service.extract_from_audio(audio.file.path)
        features_obj = type("Features", (), features_data)
        genre = classifier.predict_subgenre(features_obj)
        features_repo.create_features(audio, build_features_dict(features_data))
    song, _ = song_repo.create_song(user, audio, title, artist)
    
    if genre:
        song.genre = genre
        song.save(update_fields=["genre"])
    
    return song