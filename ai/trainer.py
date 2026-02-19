import joblib
from lightgbm import LGBMClassifier

MODEL_PATH = "models/model.pkl"

def train_model(X, y):
    model = LGBMClassifier()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
