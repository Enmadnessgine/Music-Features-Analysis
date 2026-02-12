from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.svm import SVC

MODELS = {
    "RandomForest": RandomForestClassifier,
    "AdaBoost": AdaBoostClassifier,
    "SVC": SVC,
    "ETC": ExtraTreesClassifier
}


def build_model(model_name: str, params: dict | None = None):
    cls = MODELS[model_name]

    if params is None:
        return cls()
    return cls(**params)