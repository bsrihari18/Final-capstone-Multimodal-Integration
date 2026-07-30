"""Cached ML model loading for Streamlit Cloud."""

import os
from pathlib import Path

# Keep TensorFlow on CPU and reduce log noise before import.
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import streamlit as st

from utils.constants import (
    FER_MODEL_PATH,
    LABEL_ENCODER_PATH,
    MODEL_FILES,
    RF_MODEL_PATH,
    SVC_MODEL_PATH,
    TFIDF_PATH,
    XGB_MODEL_PATH,
)


def missing_models():
    """Return human-readable names for model files that are not on disk."""
    missing = []
    for name, path in MODEL_FILES.items():
        if not Path(path).is_file():
            missing.append(f"{name} ({path})")
    return missing


@st.cache_resource(show_spinner="Loading facial emotion model…")
def load_fer_model():
    from tensorflow.keras.models import load_model

    if not Path(FER_MODEL_PATH).is_file():
        raise FileNotFoundError(f"FER model not found: {FER_MODEL_PATH}")

    return load_model(FER_MODEL_PATH)


@st.cache_resource(show_spinner="Loading text emotion models…")
def load_text_models():
    import joblib

    paths = {
        "vectorizer": TFIDF_PATH,
        "label_encoder": LABEL_ENCODER_PATH,
        "svc": SVC_MODEL_PATH,
        "rf": RF_MODEL_PATH,
        "xgb": XGB_MODEL_PATH,
    }

    for label, path in paths.items():
        if not Path(path).is_file():
            raise FileNotFoundError(f"Text model '{label}' not found: {path}")

    return {
        "vectorizer": joblib.load(TFIDF_PATH),
        "label_encoder": joblib.load(LABEL_ENCODER_PATH),
        "svc": joblib.load(SVC_MODEL_PATH),
        "rf": joblib.load(RF_MODEL_PATH),
        "xgb": joblib.load(XGB_MODEL_PATH),
    }
