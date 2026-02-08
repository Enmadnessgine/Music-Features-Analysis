class ModelRegistry:
    '''Special class to get/register models into your code.
    If you want to take the model - try method get with this params:
        "genre" - identifies subgenre
        "user_profile" - return statistics based on user profile
    If you want to register you model:
    (ATTENTION - registered model should not be pathed any files beside
    "DataModifying/models/artifacts/" to make code cleaner)
        try register method with params "name" (str) and model (Classifier.py instance)
    '''
    _models = {}

    @classmethod
    def get(cls, name):
        return cls._models[name]

    @classmethod
    def register(cls, name, model):
        cls._models[name] = model