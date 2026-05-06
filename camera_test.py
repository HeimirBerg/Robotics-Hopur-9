import cv2

# 0 is the index for /dev/video0 which we verified earlier
cap = cv2.VideoCapture(0)

# Set the resolution (Optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    # Capture one frame
    ret, frame = cap.read()

    if ret:
        # Save the image to your desktop
        cv2.imwrite('/home/pi/Desktop/opencv_capture.jpg', frame)
        print("Success! Image saved to Desktop.")
    else:
        print("Error: Could not read frame.")

# Release the hardware
cap.release()