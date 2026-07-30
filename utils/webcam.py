import cv2
import numpy as np
from PIL import Image

from utils.face_detection import process_frame


class EmotionProcessor:
    """
    Processes images captured from Streamlit camera_input().
    """

    @staticmethod
    def process(uploaded_image):
        """
        uploaded_image : UploadedFile returned by st.camera_input()
        """

        if uploaded_image is None:
            return None

        # Convert uploaded image to numpy array
        image = Image.open(uploaded_image).convert("RGB")
        image = np.array(image)

        # RGB -> BGR (OpenCV format)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Detect face + predict emotion
        image = process_frame(image)

        return image
