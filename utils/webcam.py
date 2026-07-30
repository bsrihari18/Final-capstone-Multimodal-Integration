from streamlit_webrtc import VideoProcessorBase
import av

from utils.face_detection import process_frame


class EmotionProcessor(VideoProcessorBase):

    def recv(self, frame):

        image = frame.to_ndarray(format="bgr24")

        image = process_frame(image)

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )