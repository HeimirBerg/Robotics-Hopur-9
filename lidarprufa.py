import threading
import time
from pyrplidar import PyRPlidar

# --- LiDAR configuration ---
LIDAR_PORT = "/dev/ttyUSB0"
BAUDRATE   = 1000000
MOTOR_PWM  = 660

# --- Sectors (degrees) — adjust if LiDAR is mounted differently ---
# 0° is assumed to be the front of the robot
FRONT_SECTOR      = (345, 15)    # directly ahead  ±15°
FRONT_LEFT_SECTOR = (315, 345)   # front-left
FRONT_RIGHT_SECTOR = (15, 45)    # front-right

MAX_RANGE_CM = 300   # ignore readings beyond this

# --- Shared state ---
_scan_data = {}          # angle(int) -> distance(cm)
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

        while _running:
            try:
                scan_gen = lidar.start_scan()
                current  = {}

                for scan in scan_gen():
                    if not _running:
                        break

                    angle_deg = round(scan.angle) % 360
                    dist_cm   = scan.distance / 10.0   # mm → cm

                    if 0 < dist_cm <= MAX_RANGE_CM:
                        current[angle_deg] = dist_cm

                    if scan.start_flag and current:
                        with _lock:
                            _scan_data.update(current)
                        current = {}

            except Exception:
                # Bad packet from generator — restart the scan and keep going
                time.sleep(0.1)
                continue

    except Exception as e:
        print(f"LiDAR connection error: {e}")
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
    time.sleep(2)   # wait for first full scan


def stop_lidar():
    global _running
    _running = False
    if _thread:
        _thread.join(timeout=3)


def _sector_min(start_angle, end_angle):
    """Return the minimum distance (cm) within a degree sector."""
    with _lock:
        data = dict(_scan_data)

    if start_angle <= end_angle:
        values = [v for k, v in data.items() if start_angle <= k <= end_angle]
    else:
        # Wraps around 0° (e.g. 345° → 15°)
        values = [v for k, v in data.items() if k >= start_angle or k <= end_angle]

    return min(values) if values else MAX_RANGE_CM


def sense():
    """
    Return the nearest obstacle distance (cm) in three sectors:
        front       — directly ahead
        front_left  — ahead and to the left
        front_right — ahead and to the right
    """
    front       = _sector_min(*FRONT_SECTOR)
    front_left  = _sector_min(*FRONT_LEFT_SECTOR)
    front_right = _sector_min(*FRONT_RIGHT_SECTOR)
    return front, front_left, front_right