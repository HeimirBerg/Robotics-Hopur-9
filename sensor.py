import threading
import time
from pyrplidar import PyRPlidar

LIDAR_PORT = "/dev/ttyUSB0"
BAUDRATE   = 1000000

_scan_data = {}        # angle(int) -> distance(cm)
_lock      = threading.Lock()
_running   = False

def LiDAR_data():
    lidar = PyRPlidar()
    lidar.connect(port=LIDAR_PORT, baudrate=BAUDRATE, timeout=3)
    lidar.reset()
    time.sleep(5)
    lidar.lidar_serial._serial.reset_input_buffer()

    scan_gen = lidar.start_scan()

    for scan in scan_gen():
        if not _running:
            break
        angle    = round(scan.angle) % 360
        distance = scan.distance / 10.0  # mm -> cm
        with _lock:
            _scan_data[angle] = distance

    lidar.stop()
    lidar.disconnect()