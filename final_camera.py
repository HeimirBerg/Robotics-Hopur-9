import cv2
import time

# 1. Initialize with the V4L2 backend
# This is the most stable way to talk to the ov5647 on Trixie
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# 2. Set the resolution to the sensor's native aspect ratio
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Could not open camera. Make sure no other apps are using it.")
else:
    print("Camera warmed up... taking photo in 2 seconds.")
    
    # Let the auto-exposure settle
    time.sleep(2) 
    
    # Clear the buffer by grabbing a few frames
    for _ in range(5):
        cap.read()

    # Capture the actual image
    ret, frame = cap.read()

    if ret:
        # Save to your home directory
        cv2.imwrite('pi_camera_victory.jpg', frame)
        print("Success! 'pi_camera_victory.jpg' is in your current folder.")
    else:
        print("Failed to capture image.")

cap.release()