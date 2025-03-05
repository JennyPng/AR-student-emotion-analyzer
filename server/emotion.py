import cv2
import numpy as np

# webcam
cap = cv2.VideoCapture(0)  # 0 for default webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # display webcam
    cv2.imshow("Emotion Analyzer", frame)

    # q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):  
        break
cap.release()
cv2.destroyAllWindows()