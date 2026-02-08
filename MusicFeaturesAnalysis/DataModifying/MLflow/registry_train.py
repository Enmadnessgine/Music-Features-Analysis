TRAINERS = {}

def register(name):
    def wrapper(func):
        TRAINERS[name] = func
        return func
    return wrapper


def get_trainer(name):
    if name not in TRAINERS:
        raise ValueError(f"Unknown model: {name}")
    return TRAINERS[name]


from DataModifying.MLflow import train_genre
from DataModifying.MLflow import train_subgenre