import joblib 
import numpy as np 
from utils.integration_rules import integrate_text_predictions

from utils.constants import (
    TFIDF_PATH,
    LABEL_ENCODER_PATH,
    SVC_MODEL_PATH,
    RF_MODEL_PATH,
    XGB_MODEL_PATH
)

from utils.text_preprocessing import preprocess_text


# Load Models
vectorizer = joblib.load(TFIDF_PATH)

label_encoder = joblib.load(LABEL_ENCODER_PATH)

svc_model = joblib.load(SVC_MODEL_PATH)

rf_model = joblib.load(RF_MODEL_PATH)

xgb_model = joblib.load(XGB_MODEL_PATH)


def predict_text_emotion(text):

    processed = preprocess_text(text)

    vector = vectorizer.transform([processed])

    svc_prediction = svc_model.predict(vector)[0]

    rf_prediction = rf_model.predict(vector)[0]

    xgb_prediction = xgb_model.predict(vector)[0]

    # Convert XGBoost integer prediction to emotion name
    if isinstance(xgb_prediction, (int, np.integer)):
        xgb_prediction = label_encoder.inverse_transform([xgb_prediction])[0]

    final_prediction = integrate_text_predictions(
        svc_prediction,
        rf_prediction,
        xgb_prediction
    )

    return (
        svc_prediction,
        rf_prediction,
        xgb_prediction,
        final_prediction
    )