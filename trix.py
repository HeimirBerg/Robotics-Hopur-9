import cv2
from picamera2 import Picamera2
import os

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

print("Camera running in Safe Mode...")

try:
    # Set the environment variable for the display inside Python
    os.environ["QT_QPA_PLATFORM"] = "wayland" # or "xcb"
    
    while True:
        frame = picam2.capture_array()
        
        # This is the line that's crashing. 
        # If it still crashes, comment out the next two lines 
        # and uncomment the imwrite line to just save files.
        cv2.imshow('Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        # cv2.imwrite("live_check.jpg", frame) 
except Exception as e:
    print(f"Error: {e}")
finally:
    picam2.stop()
    cv2.destroyAllWindows()