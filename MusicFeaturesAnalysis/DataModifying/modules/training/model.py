
import pickle

def upload(path, model, model_name):
    with open(f"{path}/{model_name}.pkl", "wb") as f:
        pickle.dump(model, f)
