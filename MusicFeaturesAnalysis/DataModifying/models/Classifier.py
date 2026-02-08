from collections import defaultdict
import pandas as pd
from DataModifying.models.ModelRegistry import ModelRegistry
from DataModifying.models.config import FEATURE_COLS, GROUPS
from mainapp.models import AudioFile, Song
from abc import ABC, abstractmethod
import joblib
from DataModifying.modules.preprocessing.genre_mapping import GENRE_TO_GROUP
import math

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

    def predict(self, user) -> dict[str, int | float | list]:
        '''Takes ALL information about user from DB and works with prediction.
        Returns dictionary, which has root genres with their probabilities to appear in
        user account (basic mean) and with subgenre as a key and list as a value. The list has
        dict with subgenres as key and percentage of subgenre as value. It'll give a lot of fun with statistics!
        :param user: User instance (basic django.contrib.auth.models.User)
        :return: list of dicts with special order, sorted by percentage of root genre
        :rtype list
        '''
        songs = Song.objects.filter(user=user).select_related('audio__features')

        if not songs:
            return {}

        subgenre_sum = defaultdict(int)
        macrogenre_sum = defaultdict(int)
        total_mood = 0

        for s in songs:
            f = s.audio.features
            mood_raw = (0.4 * f.energy + 0.3  * f.valence + 0.2 *
                    f.danceability - 0.1 * f.liveness)
            total_mood += mood_raw + 0.1

            subgenre_sum[s.genre] += 1
            group = GENRE_TO_GROUP.get(s.genre)
            macrogenre_sum[group] += 1


        count = len(songs)
        genres_statistics = []

        for macro, subs in GROUPS.items():
            if macrogenre_sum[macro] > 0:
                current_subgenres = {
                    genre: round(count_val / count, 2)
                    for genre, count_val in subgenre_sum.items()
                    if GENRE_TO_GROUP.get(genre) == macro
                }

                genres_statistics.append({
                    "macro_genre": macro,
                    "percentage": round(macrogenre_sum[macro] / count, 2),
                    "subgenres": current_subgenres
                })



        all_p = [val / count for val in subgenre_sum.values()]
        entropy = -sum(p * math.log2(p) for p in all_p if p > 0)
        h_max = math.log2(len(all_p)) if len(all_p) > 1 else 1
        diversity_score = round(entropy / h_max, 3)


        return {
            "count": count,
            "genres": sorted(genres_statistics, key=lambda x: x["percentage"], reverse=True),
            "top_macro_genre": genres_statistics[0]["macro_genre"] if genres_statistics else None,
            "top_subgenre": max(subgenre_sum, key=subgenre_sum.get) if subgenre_sum else None,
            "diversity_score": diversity_score,
            "mood": round(total_mood / count, 3)
        }


