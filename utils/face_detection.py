import cv2
import numpy as np
from utils.fer_prediction import predict_emotion

# --------------------------------------------------
# Shared Variables
# --------------------------------------------------
CURRENT_FACE_EMOTION = "No Face"
CURRENT_FACE_CONFIDENCE = 0.0

# --------------------------------------------------
# Haar Cascade
# --------------------------------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# --------------------------------------------------
# Detect Faces
# --------------------------------------------------
def detect_faces(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(60, 60)
    )

    return gray, faces


# --------------------------------------------------
# Process Image
# --------------------------------------------------
def process_frame(frame):

    global CURRENT_FACE_EMOTION
    global CURRENT_FACE_CONFIDENCE

    gray, faces = detect_faces(frame)

    if len(faces) == 0:

        CURRENT_FACE_EMOTION = "No Face"
        CURRENT_FACE_CONFIDENCE = 0.0

        return frame

    best_face = None
    best_area = 0

    for (x, y, w, h) in faces:

        area = w * h

        if area > best_area:

            best_area = area
            best_face = (x, y, w, h)

    x, y, w, h = best_face

    face = gray[y:y+h, x:x+w]

    emotion, confidence = predict_emotion(face)

    CURRENT_FACE_EMOTION = emotion
    CURRENT_FACE_CONFIDENCE = confidence

    confidence_percent = confidence * 100

    cv2.rectangle(
        frame,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        2
    )

    label = f"{emotion} ({confidence_percent:.2f}%)"

    cv2.putText(
        frame,
        label,
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    return frame


# --------------------------------------------------
# Get Latest Face Prediction
# --------------------------------------------------
def get_current_face_prediction():

    return CURRENT_FACE_EMOTION, CURRENT_FACE_CONFIDENCE
