from picamera2 import Picamera2
import time

# 1. Initialize the camera
picam2 = Picamera2()

# 2. Configure for a standard preview (640x480 is fast and clear)
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)

# 3. Start the Window and the Camera
# We use 'qt' for standard desktop environments
picam2.start_preview(picam2.create_qt_preview())
picam2.start()

print("Live feed started! Press Ctrl+C in this terminal to stop.")

try:
    # Keep the script running so the window stays open
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nClosing camera...")
finally:
    # Always cleanup to release the hardware for next time
    picam2.stop_preview()
    picam2.stop()