from picamera2 import Picamera2
import time

# 1. Setup the camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)

# 2. Start the preview window
# We use 'qt' because you are likely on a Desktop environment/VNC
picam2.start_preview(picam2.create_qt_preview())

# 3. Start the actual camera stream
picam2.start()

print("Displaying camera feed. Press Ctrl+C in the terminal to stop.")

try:
    while True:
        time.sleep(1) # Keep the script alive so the window stays open
except KeyboardInterrupt:
    print("Stopping...")
finally:
    picam2.stop_preview()
    picam2.stop()