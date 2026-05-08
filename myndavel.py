import cv2
from picamera2 import Picamera2


# 1. Initialize Picamera2 (The "Brain")
picam2 = Picamera2()

# 2. Configure the stream
# This tells the ISP to turn the Raw Bayer into a standard image for us
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)

# 3. Start the camera
picam2.start()

print("Camera Live! Press 'q' to quit.")

try:
    while True:
        # Capture a frame into a format OpenCV understands (NumPy array)
        frame = picam2.capture_array()

        # Display the frame in a window
        cv2.imshow('Robotics-Hopur-9 Live Feed', frame)

        # Stop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("\nInterrupted by user.")
finally:
    # Always stop the hardware properly
    picam2.stop()
    cv2.destroyAllWindows()