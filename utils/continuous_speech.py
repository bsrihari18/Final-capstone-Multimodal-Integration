import threading
import time

from utils.speech_buffer import SpeechBuffer
from utils.speech_recognition import recognize_speech
from utils.text_prediction import predict_text_emotion


class ContinuousSpeech:

    def __init__(self, interval=5):

        self.interval = interval
        self.buffer = SpeechBuffer()

        self.running = False
        self.thread = None

    def _run(self):

        print("[Speech Thread] Started")

        while self.running:

            try:

                text = recognize_speech()

                if not text:
                    time.sleep(1)
                    continue

                text = text.strip()

                if text == "":
                    time.sleep(1)
                    continue

                result = predict_text_emotion(text)

                if isinstance(result, tuple):
                    emotion = result[-1]
                else:
                    emotion = result

                self.buffer.add_prediction(
                    emotion=emotion,
                    text=text
                )

                print(f"[Speech] Text    : {text}")
                print(f"[Speech] Emotion : {emotion}")

            except Exception as e:

                print(f"[Speech Error] {e}")
                time.sleep(2)

            time.sleep(self.interval)

        print("[Speech Thread] Stopped")

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            daemon=True,
            name="ContinuousSpeechThread"
        )

        self.thread.start()

    def stop(self):

        self.running = False

        if self.thread is not None:
            self.thread.join(timeout=1)

    def get_summary(self):

        return self.buffer.get_summary()

    def clear(self):

        self.buffer.clear()
