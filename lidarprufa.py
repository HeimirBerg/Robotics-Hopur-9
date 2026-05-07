import threading
import time
from pyrplidar import PyRPlidar

# --- Configuration ---
LIDAR_PORT = "/dev/ttyUSB0"
BAUDRATE   = 1000000
MAX_RANGE  = 300   # cm — ignore anything beyond this

# --- Thresholds (cm) ---
TOO_CLOSE = 30   # back up if everything is this close
TURNING   = 80   # start turning if front is closer than this

# --- Shared scan data ---
_scan_data = {}   # angle(int) -> distance(cm)
_lock      = threading.Lock()
_running   = False
_thread    = None


def _scan_worker():
    lidar = PyRPlidar()
    try:
        lidar.connect(port=LIDAR_PORT, baudrate=BAUDRATE, timeout=3)
        lidar.lidar_serial.set_dtr(False)  # enables motor on S2L
        time.sleep(1)

        scan_gen = lidar.start_scan()

        for scan in scan_gen():
            if not _running:
                break

            angle    = round(scan.angle) % 360
            distance = scan.distance / 10.0   # mm -> cm

            if 0 < distance <= MAX_RANGE:
                with _lock:
                    _scan_data[angle] = distance

    except Exception as e:
        print(f"LiDAR error: {e}")
    finally:
        try:
            lidar.lidar_serial.set_dtr(True)
            lidar.stop()
            lidar.disconnect()
            print("LiDAR disconnected.")
        except Exception:
            pass


def start_lidar():
    global _running, _thread
    _running = True
    _thread  = threading.Thread(target=_scan_worker, daemon=True)
    _thread.start()
    time.sleep(2)   # wait for first scan to arrive
    print("LiDAR ready.")


def stop_lidar():
    global _running
    _running = False
    if _thread:
        _thread.join(timeout=3)


def get_distance(start_angle, end_angle):
    """Return the nearest obstacle (cm) in a degree sector."""
    with _lock:
        data = dict(_scan_data)

    if start_angle <= end_angle:
        values = [v for k, v in data.items() if start_angle <= k <= end_angle]
    else:
        # wraps around 0 degrees (e.g. 315 -> 15)
        values = [v for k, v in data.items() if k >= start_angle or k <= end_angle]

    return min(values) if values else 999


def get_action():
    """Decide what the robot should do based on current LiDAR readings."""
    front = get_distance(345, 15)
    left  = get_distance(315, 345)
    right = get_distance(15,  45)

    if front > TURNING and left > TOO_CLOSE and right > TOO_CLOSE:
        return "forward"
    elif left > right:
        return "left"
    elif right >= left:
        return "right"
    else:
        return "back"