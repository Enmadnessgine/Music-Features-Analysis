from django.contrib.auth.models import User
from django.db import transaction
from DataModifying.models.Classifier import GenreClassifier
from ..models import AudioFile, Song, Features
from ..utils.info_utils import get_info, get_features, build_features_dict
from mainapp.services.model_db import ModelData

audio_repo = ModelData(AudioFile)
song_repo = ModelData(Song)
features_repo = ModelData(Features)

@transaction.atomic
def save_top_tracks_with_features(user: User, top_tracks: list[dict]):

    classifier = GenreClassifier(
        model_path="DataModifying/models/artifacts/genre_classifier.pkl"
    )

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

        audio, _ = audio_repo.get_or_create(
            kwargs={"file_hash": f"spotify:{spotify_id}"},
            defaults={"file": None, "size": 0},
        )

        song, created = song_repo.get_or_create(
            kwargs={
                "user": user,
                "audio": audio,
            },
            defaults={
                "track_id": spotify_id,
                "title": track["name"],
                "artist": track["artist"],
            },
        )

        if features_data:
            features_obj = type("Features", (), features_data)
            genre = classifier.predict_genre(features_obj)

            print(genre)
            
            song.genre = genre
            song.save(update_fields=["genre"])

            features_repo.get_or_update(
                kwargs={"audio": audio},
                defaults=build_features_dict(features_data),
            )

        print(f"Saved: {track['name']}")


def get_user_songs(user: User):
    return song_repo.get_all(
        filters={"user": user}, select_related=["audio", "audio__features"]
    )

def delete_user_song(user: User, song_id: int):
    return song_repo.delete(id=song_id, user=user) > 0