from pyrplidar import PyRPlidar
import threading
import time

LIDAR_PORT = "/dev/ttyUSB0"
BAUDRATE   = 1000000
MAX_RANGE  = 300  # cm

_scan_data = {}
_lock      = threading.Lock()
_running   = False

def LiDAR_data():
    global _running, _scan_data
    lidar = PyRPlidar()
    try:
        lidar.connect(port=LIDAR_PORT, baudrate=BAUDRATE, timeout=3)
        lidar.reset()
        time.sleep(5)
        lidar.lidar_serial._serial.reset_input_buffer()

        scan_gen = None
        for attempt in range(100):
            try:
                scan_gen = lidar.start_scan()
                print(f"Scan started on attempt {attempt + 1}")
                break
            except Exception:
                time.sleep(0.05)

        if scan_gen is None:
            raise Exception("Could not start scan after 100 attempts")

        _running = True

        for scan in scan_gen():
            if not _running:
                break
            angle    = round(scan.angle) % 360
            distance = scan.distance / 10.0
            if 0 < distance <= MAX_RANGE:
                with _lock:
                    _scan_data[angle] = distance
                yield angle, distance

    except KeyboardInterrupt:
        pass
    finally:
        _running = False
        lidar.stop()
        lidar.disconnect()

def get_snapshot():
    with _lock:
        return dict(_scan_data)

def any_under(snapshot, zone, threshold):
    return any(dist < threshold for angle, dist in snapshot.items() if angle in zone)

def zone_clearance(snapshot, zone):
    distances = [dist for angle, dist in snapshot.items() if angle in zone]
    return sum(distances) / len(distances) if distances else MAX_RANGE