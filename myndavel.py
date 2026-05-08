import cv2
from picamera2 import Picamera2
from flask import Flask, Response

# 1. Setup Camera (No window will be opened)
print("Initializing Camera...")
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()
print("Camera started successfully!")

app = Flask(__name__)

def generate_frames():
    while True:
        # Capture frame
        frame = picam2.capture_array()
        
        # Convert to JPEG for the web
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()

        # Yield the output in MJPEG format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    # Simple HTML page to display the stream
    return "<html><body style='background:#222; color:white; text-align:center;'>" \
           "<h1>Robotics-Hopur-9 Live</h1>" \
           "<img src='/video_feed' style='border:2px solid red;'>" \
           "</body></html>"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Web server launching at http://10.98.208.33:5000")
    try:
        # We use 0.0.0.0 to listen on all network interfaces
        app.run(host='0.0.0.0', port=5000, threaded=True)
    finally:
        picam2.stop()