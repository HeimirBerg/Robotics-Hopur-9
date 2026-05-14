import cv2
from picamera2 import Picamera2
from flask import Flask, Response
import sys



# Uppsetning myndavélar
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

app = Flask(__name__)

def generate_frames():
    while True:
        # Tökum mynd
        frame = picam2.capture_array()
        # Breytum í JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        # Setjum úrtakið á MJPEG form
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/streymi')
def streymi(): 
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Einföld HTML síða til að skoða streymið
    return "<html><body style='background:#222; color:white; text-align:center;'>" \
        "<h1>Robotics-Hopur-9 Live</h1>" \
        "<img src='/video_feed' style='border:2px solid red;'>" \
        "</body></html>"

if __name__ == '__main__':
    # Síðan er á  http://10.98.208.33:5000
    app.run(host='0.0.0.0', port = 5000, threaded=True)
    picam2.stop()