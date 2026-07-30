from collections import Counter


class AnalyticsManager:

    def __init__(self):

        pass

    def emotion_counts(self, history):

        emotions = [

            row["final_emotion"]

            for row in history

        ]

        return dict(Counter(emotions))

    def face_counts(self, history):

        emotions = [

            row["face_emotion"]

            for row in history

        ]

        return dict(Counter(emotions))

    def speech_counts(self, history):

        emotions = [

            row["speech_emotion"]

            for row in history

        ]

        return dict(Counter(emotions))

    def dominant_emotion(self, history):

        counts = self.emotion_counts(history)

        if len(counts) == 0:
            return "No Data"

        return max(
            counts,
            key=counts.get
        )

    def total_windows(self, history):

        return len(history)