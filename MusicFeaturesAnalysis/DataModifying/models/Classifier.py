from collections import defaultdict
import pandas as pd
from DataModifying.models.ModelRegistry import ModelRegistry
from DataModifying.models.config import FEATURE_COLS, GROUPS, VECTOR_FIELDS
from mainapp.models import Song, Statistics
import joblib
from DataModifying.modules.preprocessing.genre_mapping import GENRE_TO_GROUP
import math
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


# for predict() method.
def return_top_genre(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if not isinstance(result, dict) or not result:
            raise ValueError("Expected non-empty dict")

        return max(result, key=result.get)

    return wrapper


class GenreClassifier:

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


class UserGenreAggregator:
    def _mood_label(self, x):
        if x < 0.3:
            return "sad"
        elif x < 0.6:
            return "neutral"
        return "happy"

    def _embedding(self, mean_features: list, mood: float, all_macrogenre_percent: dict, all_subgenre_percent: dict):
        all_macrogenres_list = ['calm', 'vocal', 'acoustic', 'energetic']
        all_subgenres_list = ["pop", "reggae", "rap", 'hip-hop', "electronic", "rock", "ambient", "classical", "jazz",
                              "folk"]
        macro_vector = [all_macrogenre_percent.get(g, 0.0) for g in all_macrogenres_list]
        sub_vector = [all_subgenre_percent.get(g, 0.0) for g in all_subgenres_list]
        user_vector = mean_features + macro_vector + sub_vector + [mood]
        return user_vector

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
        sum_features = defaultdict(float)
        total_mood = 0

        for s in songs:
            f = s.audio.features
            mood_raw = (0.4 * f.energy + 0.3 * f.valence + 0.2 *
                        f.danceability - 0.1 * f.liveness)
            total_mood += mood_raw + 0.1

            subgenre_sum[s.genre] += 1
            group = GENRE_TO_GROUP.get(s.genre)
            macrogenre_sum[group] += 1

            sum_features['energy'] += f.energy
            sum_features['acousticness'] += f.acousticness
            sum_features['tempo'] += f.tempo
            sum_features['danceability'] += f.danceability
            sum_features['instrumentalness'] += f.instrumentalness
            sum_features['loudness'] += f.loudness
            sum_features['liveness'] += f.liveness
            sum_features['speechiness'] += f.speechiness
            sum_features['valence'] += f.valence

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
        mood = round(total_mood / count, 3)

        mean_features = {val: round(key / count, 2) for val, key in sum_features.items()}

        all_subgenre_percent = {val: round(key / count, 2) for val, key in subgenre_sum.items()}
        all_macrogenre_percent = {val: round(key / count, 2) for val, key in macrogenre_sum.items() if key != 0}
        emb = self._embedding(list(mean_features.values()), mood, all_macrogenre_percent, all_subgenre_percent)

        return {
            "count": count,
            "genres": sorted(genres_statistics, key=lambda x: x["percentage"], reverse=True),
            "top_macro_genre": genres_statistics[0]["macro_genre"] if genres_statistics else None,
            "top_macro_genre_percent": genres_statistics[0]["percentage"] if genres_statistics else None,
            "top_subgenre": max(subgenre_sum, key=subgenre_sum.get) if subgenre_sum else None,
            "top_subgenre_percent": round(max(all_p), 2),
            "rarest_subgenre": min(subgenre_sum, key=subgenre_sum.get) if subgenre_sum else None,
            "diversity_score": diversity_score,
            "mood": mood,
            "mood_labeled": self._mood_label(mood),
            "all_subgenre_percent": all_subgenre_percent,
            "all_macrogenre_percent": all_macrogenre_percent,
            "mean_features": mean_features,
            "user_vector": np.array(emb, dtype=float)
        }


def similarity(user, user_similarity=False):
    user_vector_raw = Statistics.objects.filter(user=user).values_list('user_vector', flat=True).first()

    if not user_vector_raw:
        return [], []

    user_vec = np.array(user_vector_raw)

    if user_similarity:
        data = Statistics.objects.exclude(user=user).values_list('user_id', 'user_vector')
    else:
        data = Song.objects.values_list('id', *VECTOR_FIELDS)

    ids = [item[0] for item in data]
    all_vectors = np.array([item[1] if user_similarity else item[1:] for item in data])

    scaler = StandardScaler()
    all_vectors_scaled = scaler.fit_transform(all_vectors)
    user_vec_scaled = scaler.transform(user_vec.reshape(1, -1))

    sim = cosine_similarity(user_vec_scaled, all_vectors_scaled)
    top_idx = sim.argsort()[0][-5:][::-1]
    top_ids = [ids[i] for i in top_idx]
    return top_ids
