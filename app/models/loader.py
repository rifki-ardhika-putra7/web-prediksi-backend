import joblib
import os

def load_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "model_kelulusan_balanced.pkl")
    return joblib.load(model_path)
