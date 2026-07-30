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
    6: "Surprise"
}

# ============================
# Model Paths
# ============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODELS_DIR = os.path.join(BASE_DIR, "models")

FER_MODEL_PATH = os.path.join(MODELS_DIR, "fer_model.keras")

SVC_MODEL_PATH = os.path.join(MODELS_DIR, "svc_model.pkl")

RF_MODEL_PATH = os.path.join(MODELS_DIR, "random_forest_model.pkl")

XGB_MODEL_PATH = os.path.join(MODELS_DIR, "xgboost_model.pkl")

VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")

LABEL_ENCODER_PATH = os.path.join(MODELS_DIR, "label_encoder.pkl") 

# -----------------------------
# Text Model Paths
# -----------------------------

SVC_MODEL_PATH = "models/svc_model.pkl"

RF_MODEL_PATH = "models/random_forest_model.pkl"

XGB_MODEL_PATH = "models/xgboost_model.pkl"

TFIDF_PATH = "models/tfidf_vectorizer.pkl"

LABEL_ENCODER_PATH = "models/label_encoder.pkl"

# ============================
# Haar Cascade
# ============================

CASCADE_PATH = "haarcascade_frontalface_default.xml"