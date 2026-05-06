from picamera2 import Picamera2
import time

# 1. Initialize the camera 'brain'
picam2 = Picamera2()

# 2. Setup the camera (this handles the Raw-to-JPEG conversion automatically)
# We use a modest resolution to keep things fast
config = picam2.create_preview_configuration(main={"size": (1280, 720)})
picam2.configure(config)

# 3. Start the camera
picam2.start()

# 4. Capture a photo
print("Capturing photo in 2 seconds...")
time.sleep(2)
picam2.capture_file("victory.jpg")

# 5. Cleanup
picam2.stop()
print("Success! Check your folder for victory.jpg")