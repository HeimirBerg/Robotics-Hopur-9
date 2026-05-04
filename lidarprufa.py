import threading
import time
from rplidar import RPLidar

# --- Configuration ---
LIDAR_PORT = '/dev/ttyUSB0'
BAUDRATE = 1000000
CLEAR_THRESHOLD = 100
TOO_CLOSE = 20
HEADING_OFFSET = 0

FRONT_ZONE  = (330, 30)
LEFT_ZONE   = (30, 150)
RIGHT_ZONE  = (210, 330)

MIN_QUALITY = 10

_lidar = None
_latest_scan = []
_scan_lock = threading.Lock()
_running = False

def _scan_worker():
    global _running
    try:
        for scan in _lidar.iter_scans():
            if not _running:
                break
            filtered = []
            for quality, angle, dist_mm in scan:
                if quality < MIN_QUALITY or dist_mm <= 0:
                    continue
                adjusted_angle = (angle + HEADING_OFFSET) % 360
                filtered.append((quality, adjusted_angle, dist_mm))
            with _scan_lock:
                _latest_scan[:] = filtered
    except Exception as e:
        print(f"LiDAR scan error: {e}")

def start_lidar():
    global _lidar, _running
    _lidar = RPLidar(LIDAR_PORT, baudrate=BAUDRATE)
    _running = True
    t = threading.Thread(target=_scan_worker, daemon=True)
    t.start()
    time.sleep(2)
    print("LiDAR ready")

def stop_lidar():
    global _running
    _running = False
    time.sleep(0.5)
    if _lidar:
        _lidar.stop()
        _lidar.disconnect()

def _min_dist_in_zone(scan, angle_start, angle_end):
    distances = []
    for _, angle, dist_mm in scan:
        if angle_start > angle_end:
            in_zone = angle >= angle_start or angle <= angle_end
        else:
            in_zone = angle_start <= angle <= angle_end
        if in_zone:
            distances.append(dist_mm / 10.0)
    return min(distances) if distances else 999

def sense(last1=200, last2=200):
    with _scan_lock:
        scan = list(_latest_scan)
    if not scan:
        return last1, last2, 0
    front_dist = _min_dist_in_zone(scan, *FRONT_ZONE)
    left_dist  = _min_dist_in_zone(scan, *LEFT_ZONE)
    right_dist = _min_dist_in_zone(scan, *RIGHT_ZONE)
    s0 = min(left_dist, front_dist)
    s1 = min(right_dist, front_dist)
    if s0 <= 0 or s0 > 300:
        s0 = last1
    if s1 <= 0 or s1 > 300:
        s1 = last2
    merki = 1 if (front_dist < TOO_CLOSE or left_dist < TOO_CLOSE or right_dist < TOO_CLOSE) else 0
    return s0, s1, merki