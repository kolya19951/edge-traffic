import cv2

cap = cv2.VideoCapture(0)

def get_frame():
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Camera error")
    return frame
