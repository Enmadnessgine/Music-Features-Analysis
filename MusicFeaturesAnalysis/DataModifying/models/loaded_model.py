import pickle
from pathlib import Path

current_file = Path(__file__).resolve()

models_dir = current_file.parent


def rf_genre_classifier():
    artifacts_dir = models_dir / "artifacts/genre_classifier.pkl"
    with open(artifacts_dir, "rb") as f:
        model = pickle.load(f)
    return model