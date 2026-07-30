import cv2
import numpy as np
from tensorflow.keras.models import load_model

from utils.constants import FER_MODEL_PATH, IMG_SIZE, EMOTIONS


# -----------------------------
# Load FER Model
# -----------------------------
model = load_model(FER_MODEL_PATH)


# -----------------------------
# Predict Emotion
# -----------------------------
def predict_emotion(face):

    # Resize face
    face = cv2.resize(face, (IMG_SIZE, IMG_SIZE))

    # Normalize
    face = face.astype("float32") / 255.0

    # Shape -> (48,48,1)
    face = np.expand_dims(face, axis=-1)

    # Shape -> (1,48,48,1)
    face = np.expand_dims(face, axis=0)

    # Prediction
    prediction = model.predict(face, verbose=0)[0]

    emotion_index = np.argmax(prediction)

    confidence = float(np.max(prediction))

    emotion = EMOTIONS[emotion_index]

    return emotion, confidence