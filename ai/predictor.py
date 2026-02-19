import joblib
import os

MODEL_PATH = "models/model.pkl"

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None
