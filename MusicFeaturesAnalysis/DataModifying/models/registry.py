from DataModifying.models.Classifier import GenreClassifier, UserGenreAggregator
from DataModifying.models.ModelRegistry import ModelRegistry

genre_model = GenreClassifier("DataModifying/models/artifacts/genre_classifier.pkl")

ModelRegistry.register("genre", genre_model)
ModelRegistry.register(
    "user_profile",
    UserGenreAggregator(genre_model)
)
