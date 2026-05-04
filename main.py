import threading
import time
from rplidar import RPLidar

# --- Configuration ---
LIDAR_PORT = '/dev/ttyUSB0'
BAUDRATE = 1000000
CLEAR_THRESHOLD = 100   # cm - anything above this is considered clear
TOO_CLOSE = 20          # cm - danger zone, triggers merki=1

# Angular zones in degrees (0° = front of robot, clockwise)
# Adjust HEADING_OFFSET if your LiDAR is not mounted facing forward
HEADING_OFFSET = 0

FRONT_ZONE  = (330, 30)   # narrow cone directly ahead (wraps around 0°)
LEFT_ZONE   = (30, 150)   # left side
RIGHT_ZONE  = (210, 330)  # right side

MIN_QUALITY = 10          # ignore low-confidence readings

# --- Internal state ---
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
                _latest_scan[:] = filtered  # modify in place to keep reference valid
    except Exception as e:
        print(f"LiDAR scan error: {e}")


def start_lidar():
    """Start the LiDAR and background scanning thread. Call once at startup."""
    global _lidar, _running
    _lidar = RPLidar(LIDAR_PORT, baudrate=BAUDRATE)
    _running = True
    t = threading.Thread(target=_scan_worker, daemon=True)
    t.start()
    time.sleep(2)
    print("LiDAR ready")


def stop_lidar():
    """Stop the LiDAR cleanly."""
    global _running
    _running = False
    time.sleep(0.5)
    if _lidar:
        _lidar.stop()
        _lidar.disconnect()


def _min_dist_in_zone(scan, angle_start, angle_end):
    """Return minimum distance (cm) of all points within an angular zone."""
    distances = []
    for _, angle, dist_mm in scan:
        if angle_start > angle_end:  # zone wraps around 0° (e.g. front zone)
            in_zone = angle >= angle_start or angle <= angle_end
        else:
            in_zone = angle_start <= angle <= angle_end
        if in_zone:
            distances.append(dist_mm / 10.0)  # mm -> cm
    return min(distances) if distances else 999


def sense(last1=200, last2=200):
    """
    Returns (s0, s1, merki) - drop-in replacement for the ultrasonic sense().
    s0 = left side clearance in cm
    s1 = right side clearance in cm
    merki = 1 if anything is dangerously close, else 0
    """
    with _scan_lock:
        scan = list(_latest_scan)

    if not scan:
        return last1, last2, 0

    front_dist = _min_dist_in_zone(scan, *FRONT_ZONE)
    left_dist  = _min_dist_in_zone(scan, *LEFT_ZONE)
    right_dist = _min_dist_in_zone(scan, *RIGHT_ZONE)

    # s0 and s1 reflect side clearance, capped by what's ahead
    s0 = min(left_dist, front_dist)
    s1 = min(right_dist, front_dist)

    # Clamp bad readings to last known good value
    if s0 <= 0 or s0 > 300:
        s0 = last1
    if s1 <= 0 or s1 > 300:
        s1 = last2

    merki = 1 if (front_dist < TOO_CLOSE or left_dist < TOO_CLOSE or right_dist < TOO_CLOSE) else 0

    return s0, s1, merki