import numpy as np

from utils.integration_rules import integrate_text_predictions
from utils.model_loader import load_text_models
from utils.text_preprocessing import preprocess_text


def predict_text_emotion(text):
    models = load_text_models()

    processed = preprocess_text(text)
    vector = models["vectorizer"].transform([processed])

    svc_prediction = models["svc"].predict(vector)[0]
    rf_prediction = models["rf"].predict(vector)[0]
    xgb_prediction = models["xgb"].predict(vector)[0]

    if isinstance(xgb_prediction, (int, np.integer)):
        xgb_prediction = models["label_encoder"].inverse_transform(
            [xgb_prediction]
        )[0]

    final_prediction = integrate_text_predictions(
        svc_prediction,
        rf_prediction,
        xgb_prediction,
    )

    return svc_prediction, rf_prediction, xgb_prediction, final_prediction
