from DataModifying.modules.preprocessing.clip import clip_outliers_iqr
from collections import defaultdict
import pandas as pd
from loaded_model import model
from config import FEATURE_COLS, GENRES
from mainapp.models import Features, AudioFile, Song


def predict_song_genre(audio_or_features) -> dict[str, float]:
    r'''Predict genre of one song.
    :param audio_or_features: AudioFile or Features instance about song
    :return Dictionary with genre as key and percent as value
    :rtype dict
    '''
    if isinstance(audio_or_features, AudioFile):
        features = audio_or_features.features
    else:
        features = audio_or_features

    df = pd.DataFrame([{
        col: getattr(features, col)
        for col in FEATURE_COLS
    }])

    probs = model.predict_proba(df)[0]
    return dict(zip(GENRES, probs))


def predict_user_genres_old(user):
    r'''Due to test period, old version will stay to see how new one is better.
    Takes information about user from DB (step-by-step) and works with prediction
    :param user: User instance (basic django.contrib.auth.models.User)
    :return Dictionary with genre as key and percent as value
    :rtype dict
    '''
    songs = Song.objects.filter(user=user)
    genre_sum = defaultdict(float)
    count = 0

    for song in songs:
        probs = predict_song_genre(song.audio)
        for genre, p in probs.items():
            genre_sum[genre] += p
        count += 1

    return {
        genre: round(p / count, 3)
        for genre, p in genre_sum.items()
    }


def predict_user_genres_new(user) -> dict[str, float]:
    r'''Due to test period, old version will stay to see how new one is better.
    Takes ALL information about user from DB and works with prediction
    :param user: User instance (basic django.contrib.auth.models.User)
    :return Dictionary with genre as key and percent as value
    :rtype dict
    '''
    songs = Song.objects.filter(user=user).select_related('audio__features')
    if not songs.exists():
        return {}
    genre_sum = defaultdict(float)
    count = 0

    for song in songs:
        probs = predict_song_genre(song.audio)
        for genre, p in probs.items():
            genre_sum[genre] += p
        count += 1

    return {
        genre: round(p / count, 3)
        for genre, p in genre_sum.items()
    }
