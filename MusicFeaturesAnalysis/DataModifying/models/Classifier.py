from collections import defaultdict
import pandas as pd
from DataModifying.models.ModelRegistry import ModelRegistry
from DataModifying.models.config import FEATURE_COLS, GROUPS
from mainapp.models import AudioFile, Song
from abc import ABC, abstractmethod
import joblib

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
            c: float(p)
            for c, p in zip(classes, probs)
        }
    
    @return_top_genre
    def predict_macro_genre(self, features) -> str:
        return self.predict(features)

    @return_top_genre
    def predict_subgenre(self, features) -> str:
        macro = self.predict_macro_genre(features)
        leaf = ModelRegistry.get(macro).predict(features)
        return leaf

class UserGenreAggregator(BaseModel):

    def __init__(self, genre_model: GenreClassifier):
        self.genre_model = genre_model

    def load(self):
        pass

    def predict(self, user) -> list:
        '''Takes ALL information about user from DB and works with prediction.
        Returns dictionary, which has root genres with their probabilities to appear in
        user account (basic mean) and with subgenre as a key and list as a value. The list has
        dict with subgenres as key and percentage of subgenre as value. It'll give a lot of fun with statistics!
        :param user: User instance (basic django.contrib.auth.models.User)
        :return: list of dicts with special order, sorted by percentage of root genre
        :rtype list
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
        sub_sum = defaultdict(float)

        for song in songs:
            probs = self.genre_model.predict(song.audio.features)
            for genre, p in probs.items():
                genre_sum[genre] += p

            macro = self.genre_model.predict_macro_genre(song.audio.features)
            sub_model = ModelRegistry.get(macro)
            leaf_probs = sub_model.predict(song.audio.features)

            for s_genre, p in leaf_probs.items():
                sub_sum[s_genre] += p



        count = len(songs)
        result = []
        for macro, subs in GROUPS.items():
            if genre_sum[macro] > 0:
                result.append({
                    "macro_genre": macro,
                    "percentage": round(genre_sum[macro] / count, 2),
                    "subgenres": [
                        {sub: round(sub_sum[sub] / count, 2)
                        for sub in subs if sub_sum[sub] > 0}
                    ]
                })

        return sorted(result, key=lambda x: x['percentage'], reverse=True)



