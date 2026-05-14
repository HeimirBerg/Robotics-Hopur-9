import cv2
from picamera2 import Picamera2
from flask import Flask, Response
import sys

# Uppsetning myndavélar
try:
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()
except Exception as e:
    print(f"CAMERA_INIT_FAILED: {e}")
    sys.exit(1)

app = Flask(__name__)

def generate_frames():
    while True:
        # Tökum mynd
        frame = picam2.capture_array()
        # Breytum í JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        # Setjum úrtakið á MJPEG form
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/streymi')
def streymi(): 
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Einföld HTML síða til að skoða streymið
    return "<html><body style='background:#222; color:white; text-align:center;'>" \
           "<h1>Robotics-Hopur-9 Live</h1>" \
           "<img src='/streymi' style='border:2px solid red;'>" \
           "</body></html>"

if __name__ == '__main__':
    # Síðan er á  http://10.98.208.33:5000
    try:
        # We use 0.0.0.0 to listen on all network interfaces
        app.run(host='0.0.0.0', debug=False, use_reloader=False)
    finally:
        picam2.stop()