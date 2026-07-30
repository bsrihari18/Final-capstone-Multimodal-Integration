import csv
import os


class CSVLogger:

    def __init__(self, filename="outputs/emotion_history.csv"):

        self.filename = filename

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        if not os.path.exists(filename):

            with open(filename, "w", newline="", encoding="utf-8") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "Time",
                    "Face Emotion",
                    "Face Confidence",
                    "Frames",
                    "Speech Emotion",
                    "Speech Samples",
                    "Final Emotion"
                ])

    def log(self, record):

        with open(self.filename, "a", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([

                record["time"],

                record["face_emotion"],

                record["face_confidence"],

                record["frames"],

                record["speech_emotion"],

                record["speech_count"],

                record["final_emotion"]

            ])