import threading
import time
from pyrplidar import PyRPlidar

# --- Configuration ---
LIDAR_PORT = "/dev/ttyUSB0"
BAUDRATE   = 1000000
MAX_RANGE  = 300   # cm — ignore anything beyond this

# --- Shared scan data ---
_scan_data = {}   # angle(int) -> distance(cm)
_lock      = threading.Lock()
_running   = False
_thread    = None


def _scan_worker():
    lidar = PyRPlidar()
    try:
        lidar.connect(port=LIDAR_PORT, baudrate=BAUDRATE, timeout=3)
        lidar.reset()
        time.sleep(5)

        # flush leftover reset bytes from buffer
        lidar.lidar_serial._serial.reset_input_buffer()

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
    time.sleep(8)   # wait for reset (5s) + first scan
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