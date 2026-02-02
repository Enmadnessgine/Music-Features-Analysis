from django.contrib.auth.models import User
from django.db import transaction
from DataModifying.models.Classifier import GenreClassifier
from ..models import AudioFile, Song, Features
from ..utils.info_utils import get_info, get_features, build_features_dict
from mainapp.services.model_db import ModelData
from mainapp.services.models_crud.crud import audio_repo, song_repo, features_repo

classifier = GenreClassifier(model_path="DataModifying/models/artifacts/genre_classifier_v02.pkl")

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
        except Exception as e:
            print("Features error:", e)
            features_data = None

        audio, _ = audio_repo.create_audio(f"spotify:{spotify_id}", None, 0)
        song, created = song_repo.create_song(user, audio, track["name"], track["artist"], spotify_id) 
        if features_data:
            features_obj = type("Features", (), features_data)
            genre = classifier.predict_subgenre(features_obj)
            print(genre)
            song.genre = genre
            song.save(update_fields=["genre"])
            features = features_repo.create_features(audio, build_features_dict(features_data))
        print(f"Saved: {track['name']}")

def get_user_songs(user: User):
    return song_repo.get_all(user)

def delete_user_song(user: User, song_id: int):
    return song_repo.delete(id=song_id, user=user)