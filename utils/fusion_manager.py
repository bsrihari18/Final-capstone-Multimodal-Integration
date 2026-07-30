from utils.fusion import fuse_emotions


class FusionManager:

    def __init__(self,
                 face_buffer,
                 speech_service,
                 timer):

        self.face_buffer = face_buffer
        self.speech_service = speech_service
        self.timer = timer

    # ------------------------------------------
    # Check if Window Finished
    # ------------------------------------------
    def update(self):

        if not self.timer.finished():
            return None

        # -----------------------------
        # Face Summary
        # -----------------------------
        face_result = self.face_buffer.summary()

        # -----------------------------
        # Speech Summary
        # -----------------------------
        speech_result = self.speech_service.get_summary()

        # -----------------------------
        # Final Fusion
        # -----------------------------
        final_emotion = fuse_emotions(
            face_result["emotion"],
            speech_result["emotion"]
        )

        summary = {

            "face_emotion": face_result["emotion"],

            "face_confidence": face_result["confidence"],

            "frames": face_result["frames"],

            "speech_emotion": speech_result["emotion"],

            "speech_count": speech_result["count"],

            "speech_texts": speech_result["texts"],

            "final_emotion": final_emotion

        }

        # -----------------------------
        # Reset Everything
        # -----------------------------
        self.face_buffer.reset()

        self.speech_service.clear()

        self.timer.reset()

        return summary