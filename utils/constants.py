import os

# ============================
# Image Configuration
# ============================

IMG_SIZE = 48

# ============================
# Emotion Labels
# ============================

EMOTIONS = {
    0: "Angry",
    1: "Disgust",
    2: "Fear",
    3: "Happy",
    4: "Neutral",
    5: "Sad",
    6: "Surprise",
}

# ============================
# Paths
# ============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

FER_MODEL_PATH = os.path.join(MODELS_DIR, "fer_model.keras")
SVC_MODEL_PATH = os.path.join(MODELS_DIR, "svc_model.pkl")
RF_MODEL_PATH = os.path.join(MODELS_DIR, "random_forest_model.pkl")
XGB_MODEL_PATH = os.path.join(MODELS_DIR, "xgboost_model.pkl")
TFIDF_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
LABEL_ENCODER_PATH = os.path.join(MODELS_DIR, "label_encoder.pkl")

MODEL_FILES = {
    "FER CNN": FER_MODEL_PATH,
    "SVC": SVC_MODEL_PATH,
    "Random Forest": RF_MODEL_PATH,
    "XGBoost": XGB_MODEL_PATH,
    "TF-IDF Vectorizer": TFIDF_PATH,
    "Label Encoder": LABEL_ENCODER_PATH,
}
