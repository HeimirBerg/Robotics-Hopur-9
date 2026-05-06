import threading
import time
from pyrplidar import PyRPlidar

# --- LiDAR configuration ---
LIDAR_PORT = "/dev/ttyUSB0"
BAUDRATE   = 1000000
MOTOR_PWM  = 660

# --- Sectors (degrees) — adjust if LiDAR is mounted differently ---
LEFT_SECTOR  = (315, 360)   # front-left
RIGHT_SECTOR = (0,   45)    # front-right

TOO_CLOSE_CM = 20
MAX_RANGE_CM = 300

# --- Shared state ---
_scan_data = {}
_lock      = threading.Lock()
_running   = False
_thread    = None


def _scan_worker():
    global _running
    lidar = PyRPlidar()
    try:
        lidar.connect(port=LIDAR_PORT, baudrate=BAUDRATE, timeout=3)
        print("LiDAR connected.")
        lidar.set_motor_pwm(MOTOR_PWM)
        time.sleep(1)

        scan_gen = lidar.start_scan()
        current  = {}

        for scan in scan_gen():
            if not _running:
                break

            angle_deg = round(scan.angle) % 360
            dist_cm   = scan.distance / 10.0

            if 0 < dist_cm <= MAX_RANGE_CM:
                current[angle_deg] = dist_cm

            if scan.start_flag and current:
                with _lock:
                    _scan_data.update(current)
                current = {}

    except Exception as e:
        print(f"LiDAR scan error: {e}")
    finally:
        try:
            lidar.set_motor_pwm(0)
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
    time.sleep(2)


def stop_lidar():
    global _running
    _running = False
    if _thread:
        _thread.join(timeout=3)


def _sector_min(start_angle, end_angle):
    with _lock:
        data = dict(_scan_data)

    if start_angle <= end_angle:
        values = [v for k, v in data.items() if start_angle <= k <= end_angle]
    else:
        values = [v for k, v in data.items() if k >= start_angle or k <= end_angle]

    return min(values) if values else None


def sense(last0=200, last1=200):
    left  = _sector_min(*LEFT_SECTOR)
    right = _sector_min(*RIGHT_SECTOR)

    s0 = left  if left  is not None else last0
    s1 = right if right is not None else last1

    merki = 1 if (s0 < TOO_CLOSE_CM or s1 < TOO_CLOSE_CM) else 0

    return s0, s1, merki