from datetime import datetime


class HistoryManager:

    def __init__(self):

        self.history = []

    # -----------------------------------------
    # Add New Summary
    # -----------------------------------------
    def add(self, summary):

        record = {

            "time": datetime.now().strftime("%H:%M:%S"),

            "face_emotion": summary["face_emotion"],

            "face_confidence": summary["face_confidence"],

            "frames": summary["frames"],

            "speech_emotion": summary["speech_emotion"],

            "speech_count": summary["speech_count"],

            "speech_texts": summary["speech_texts"],

            "final_emotion": summary["final_emotion"]

        }

        self.history.append(record)

    # -----------------------------------------
    # Get Complete History
    # -----------------------------------------
    def get_history(self):

        return self.history

    # -----------------------------------------
    # Get Latest Record
    # -----------------------------------------
    def latest(self):

        if len(self.history) == 0:
            return None

        return self.history[-1]

    # -----------------------------------------
    # Total Windows
    # -----------------------------------------
    def total(self):

        return len(self.history)

    # -----------------------------------------
    # Clear History
    # -----------------------------------------
    def clear(self):

        self.history.clear()