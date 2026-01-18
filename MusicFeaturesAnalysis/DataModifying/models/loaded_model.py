import pickle

with open("artifacts/genre_classifier.pkl", "rb") as f:
    model = pickle.load(f)
