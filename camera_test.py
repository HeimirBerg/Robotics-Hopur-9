from picamera2 import Picamera2

try:
    picam2 = Picamera2()
    # Auto-configure based on detected camera
    picam2.configure(picam2.create_still_configuration())
    picam2.start()
    picam2.capture_file("trixie_success.jpg")
    picam2.stop()
    print("Victory! Image saved.")
except Exception as e:
    print(f"Still hitting a wall: {e}")