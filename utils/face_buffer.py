from collections import Counter
import time


class FaceBuffer:

    def __init__(self, window_size=30):

        self.window_size = window_size
        self.start_time = time.time()

        self.emotions = []
        self.confidences = []

    # ---------------------------------------
    # Add New Prediction
    # ---------------------------------------
    def add(self, emotion, confidence):

        self.emotions.append(emotion)
        self.confidences.append(confidence)

    # ---------------------------------------
    # Check Window Finished
    # ---------------------------------------
    def window_finished(self):

        return (time.time() - self.start_time) >= self.window_size

    # ---------------------------------------
    # Window Summary
    # ---------------------------------------
    def summary(self):

        if len(self.emotions) == 0:

            return {
                "emotion": "No Face",
                "confidence": 0,
                "frames": 0
            }

        majority = Counter(self.emotions).most_common(1)[0][0]

        avg_conf = sum(self.confidences) / len(self.confidences)

        return {

            "emotion": majority,

            "confidence": round(avg_conf * 100, 2),

            "frames": len(self.emotions)
        }

    # ---------------------------------------
    # Reset Window
    # ---------------------------------------
    def reset(self):

        self.start_time = time.time()

        self.emotions.clear()

        self.confidences.clear()