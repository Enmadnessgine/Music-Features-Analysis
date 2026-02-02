from DataModifying.models.Classifier import GenreClassifier, UserGenreAggregator
from DataModifying.models.ModelRegistry import ModelRegistry

macro_model = GenreClassifier("DataModifying/models/artifacts/genre_classifier_v02.pkl")
vocal_model = GenreClassifier("DataModifying/models/artifacts/Vocal_v01.pkl")
acoustic_model = GenreClassifier("DataModifying/models/artifacts/Acoustic_v01.pkl")
energetic_model = GenreClassifier("DataModifying/models/artifacts/Energetic_v01.pkl")
calm_model = GenreClassifier("DataModifying/models/artifacts/Calm_v01.pkl")

# inference friendly. Use for prediction in project
ModelRegistry.register("genre", macro_model)
ModelRegistry.register(
    "user_profile",
    UserGenreAggregator(macro_model)
)

# Use only if you know what you do
ModelRegistry.register("vocal", vocal_model)
ModelRegistry.register("acoustic", acoustic_model)
ModelRegistry.register("energetic", energetic_model)
ModelRegistry.register("calm", calm_model)




