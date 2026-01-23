from collections import defaultdict
import pandas as pd
from DataModifying.models.config import FEATURE_COLS, ID_TO_GENRE
from mainapp.models import AudioFile, Song
from abc import ABC, abstractmethod
import joblib

from abc import ABC, abstractmethod

class BaseModel(ABC):

    @abstractmethod
    def load(self):
        """Завантаження artifacts"""
        pass

    @abstractmethod
    def predict(self, data):
        """Функція передбачення/початок ml"""
        pass


#for predict() method.
def return_top_genre(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if not isinstance(result, dict) or not result:
            raise ValueError("Expected non-empty dict")

        return max(result, key=result.get)

    return wrapper

class GenreClassifier(BaseModel):

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None

    def load(self):
        if self.model is None:
            self.model = joblib.load(self.model_path)

    def predict(self, features) -> dict[str, float]:
        r'''Predict genre of one song.
        :param features: Features instance (As example, Audiofile.features)
        :return Dictionary with genre as key and percent as value
        :rtype dict
        '''
        self.load()

        df = pd.DataFrame([{
            col: getattr(features, col)
            for col in FEATURE_COLS
        }])

        probs = self.model.predict_proba(df)[0]
        classes = self.model.classes_
        return {
            ID_TO_GENRE[c]: float(p)
            for c, p in zip(classes, probs)
        }
        # return dict(zip(classes, probs))


class UserGenreAggregator(BaseModel):

    def __init__(self, genre_model: GenreClassifier):
        self.genre_model = genre_model

    def load(self):
        pass

    def predict(self, user):
        '''Takes ALL information about user from DB and works with prediction
        :param user: User instance (basic django.contrib.auth.models.User)
        :return Dictionary with genre as key and percent as value
        :rtype dict
        '''
        songs = (
            Song.objects
            .filter(user=user)
            .select_related("audio", "audio__features")
        )

        if not songs.exists():
            return {}

        return self._predict_songs(songs)

    def _predict_songs(self, songs):
        genre_sum = defaultdict(float)

        for song in songs:
            probs = self.genre_model.predict(song.audio.features)
            for genre, p in probs.items():
                genre_sum[genre] += p

        count = len(songs)
        return {g: round(p / count, 3) for g, p in genre_sum.items()}
    

