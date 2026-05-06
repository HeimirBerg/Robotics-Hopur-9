import cv2
import os

# Force the V4L2 backend specifically
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Set the buffer size to 1 (prevents memory backlog)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Set a modest resolution to start
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Still cannot allocate memory or open camera.")
else:
    # Warm up the camera (skip a few frames to let auto-exposure settle)
    for _ in range(5):
        cap.read()
        
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('victory_opencv.jpg', frame)
        print("Success! Image saved.")
    
    cap.release()