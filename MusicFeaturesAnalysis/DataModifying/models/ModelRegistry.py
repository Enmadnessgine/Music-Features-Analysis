class ModelRegistry:
    _models = {}

    @classmethod
    def get(cls, name):
        return cls._models[name]

    @classmethod
    def register(cls, name, model):
        cls._models[name] = model