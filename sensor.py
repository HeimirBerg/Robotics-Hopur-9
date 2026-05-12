from pyrplidar import PyRPlidar
import threading
import time

LIDAR_PORT = "/dev/ttyUSB0"
BAUDRATE   = 1000000
MAX_RANGE  = 300  # cm

_lock    = threading.Lock()
_running = False

def LiDAR_data():
    global _running
    lidar = PyRPlidar()
    try:
        lidar.connect(port=LIDAR_PORT, baudrate=BAUDRATE, timeout=3)
        lidar.reset()
        time.sleep(5)
        lidar.lidar_serial._serial.reset_input_buffer()

        scan_gen = lidar.start_scan()
        _running = True

        for scan in scan_gen():
            if not _running:
                break
            angle    = round(scan.angle) % 360
            distance = scan.distance / 10.0
            if 0 < distance <= MAX_RANGE:
                yield angle, distance  # ← sends angle & distance back one at a time

    except KeyboardInterrupt:
        pass
    finally:
        _running = False
        lidar.stop()
        lidar.disconnect()