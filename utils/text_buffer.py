from collections import Counter
import time


class TextBuffer:

    def __init__(self, window_size=30):

        self.window_size = window_size
        self.start_time = time.time()

        self.predictions = []

    # ---------------------------------------
    # Add Prediction
    # ---------------------------------------
    def add(self, emotion):

        self.predictions.append(emotion)

    # ---------------------------------------
    # Check Window
    # ---------------------------------------
    def window_finished(self):

        return (time.time() - self.start_time) >= self.window_size

    # ---------------------------------------
    # Summary
    # ---------------------------------------
    def summary(self):

        if len(self.predictions) == 0:

            return {

                "emotion": "No Speech",

                "count": 0
            }

        majority = Counter(self.predictions).most_common(1)[0][0]

        return {

            "emotion": majority,

            "count": len(self.predictions)
        }

    # ---------------------------------------
    # Reset
    # ---------------------------------------
    def reset(self):

        self.start_time = time.time()

        self.predictions.clear()