import cv2
import numpy as np

from utils.constants import EMOTIONS, IMG_SIZE
from utils.model_loader import load_fer_model


def predict_emotion(face):
    model = load_fer_model()

    face = cv2.resize(face, (IMG_SIZE, IMG_SIZE))
    face = face.astype("float32") / 255.0
    face = np.expand_dims(face, axis=-1)
    face = np.expand_dims(face, axis=0)

    prediction = model.predict(face, verbose=0)[0]
    emotion_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return EMOTIONS[emotion_index], confidence
