from collections import Counter
import threading


class SpeechBuffer:
    def __init__(self):
        self.predictions = []
        self.lock = threading.Lock()

    def add_prediction(self, emotion, text):
        with self.lock:
            self.predictions.append({
                "emotion": emotion,
                "text": text
            })

    def get_all(self):
        with self.lock:
            return self.predictions.copy()

    def get_summary(self):

        with self.lock:

            if len(self.predictions) == 0:
                return {
                    "emotion": "No Speech",
                    "count": 0,
                    "texts": []
                }

            emotions = [p["emotion"] for p in self.predictions]

            majority = Counter(emotions).most_common(1)[0][0]

            texts = [p["text"] for p in self.predictions]

            return {
                "emotion": majority,
                "count": len(self.predictions),
                "texts": texts
            }

    def clear(self):
        with self.lock:
            self.predictions.clear()