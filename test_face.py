import cv2

from utils.face_detection import process_frame

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = process_frame(frame)

    cv2.imshow("FER Test", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()